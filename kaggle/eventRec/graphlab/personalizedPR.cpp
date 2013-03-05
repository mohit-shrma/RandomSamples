#include<graphlab.hpp>
#include<set>
#include <sstream>
#include <string>
#include <fstream>

float RESTART_PROB = 0.5;
int MAX_ITER = 100;
std::string START_USER;


/*
 * describe the node i.e user id and its pagerank 
 */
struct User {
  //user id of user
  std::string userId;

  //page rank or prob of the user
  double pagerank;

  //number of the iteration
  int counter;

  //initialize user with zero page rank
  User():pagerank(0.0),counter(0) {}

  //TODO: figure out purpose of explicit keyword in c++
  explicit User(std::string id):userId(id),pagerank(0.0){}

  //save and load to make it serializable
  void save(graphlab::oarchive& oarc) const {
    oarc << userId << pagerank;
  }

  void load(graphlab::iarchive& iarc) {
    iarc >> userId >> pagerank;
  }
};


//define the graph with only node data and no edge data
typedef graphlab::distributed_graph<User, graphlab::empty> graph_type;


//parse the graph file line by line
bool lineParser(graph_type& graph, const std::string& fileName,	\
		const std::string& textLine) {
  //assign the current line as string stream
  std::stringstream strm(textLine);

  //vertex id of a node
  graphlab::vertex_id_type vId;

  //userId of the node
  std::string userId;

  //get the user id
  strm >> userId;

  //assign the name as vertex id
  //TODO: check if casting works
  vId = (graphlab::vertex_id_type)(atoi(userId.c_str()));

  //insert this node
  graph.add_vertex(vId, User(userId));

  //parse the rest of line to get the other nodes
  while(1) {
    //get other node id of outgoing edge
    graphlab::vertex_id_type otherNodeId;
    strm >> otherNodeId;
    if (strm.fail()) {
      return false;
    }
    graph.add_edge(vId, otherNodeId);
  }
  return true;
}




/*
 * personalized page rank vertex program
 * 
 */
class PersPageRankProg:
  public graphlab::ivertex_program<graph_type, double>,
  public graphlab::IS_POD_TYPE {
  
private:

  //variable to check whether to perform scatter or not
  bool performScatter;

public:
  //perform gather on all the in-edges
  edge_dir_type gather_edges(icontext_type& context,		\
			     const vertex_type& vertex) const {
    //TODO: what is icontext
    return graphlab::IN_EDGES;
  }

  
  //for each in-edge get the weighted sum of the edge
  double gather(icontext_type& context, const vertex_type& vertex,\
		edge_type& edge) const {
    return (edge.source().data().pagerank) / edge.source().num_out_edges();
  }

  
  //use rank or propagated probabilities of adjacent nodes to update self rank
  void apply(icontext_type& context, vertex_type& vertex,\
	     const gather_type& total) {
    
    //apply the total weighted by random walk prob
    double oldRank = vertex.data().pagerank;
    double newRank = (1 - RESTART_PROB) * total;
    vertex.data().pagerank = newRank;

    //increment the iteration counter
    ++vertex.data().counter;
    
    //set whether to perform scatter or not based on change in rank 
    performScatter = (std::fabs(oldRank - newRank) > 1E-4);

    //compare iteration counter with max iteration
    if (vertex.data().counter > MAX_ITER) {
      performScatter = 0;
    }

    if (vertex.data().userId.compare(START_USER) == 0) {
      //current node is the start user, give it the restart prob
      vertex.data().pagerank = RESTART_PROB;

      //TODO: convergence condition for start node, currently start node will never converge
      if (vertex.data().counter <= MAX_ITER) {
	performScatter = 1;
      }
    }


  }

  
  //this scatter depends on whether pagerank has converged or maxIteration has reached
  edge_dir_type scatter_edges(icontext_type& context,\
			      const vertex_type& vertex) const {
    if (performScatter) {
      return graphlab::OUT_EDGES;
    } else {
      return graphlab::NO_EDGES;
    }
  }

  //signal out edges to do the iteration
  void scatter(icontext_type& context, const vertex_type& vertex, edge_type& edge) const {
    context.signal(edge.target());
  }
};



class GraphWriter {
public:
  std::string save_vertex(graph_type::vertex_type v) {
    std::stringstream strm;
    if (v.data().pagerank > 0) {
      strm << v.data().userId << "\t" << v.data().pagerank << "\n";
      return strm.str();
    }
      return "";
  }

  std::string save_edge(graph_type::edge_type e) {return "";}
};


//parse a file to return the users set to work on
std::set<std::string> getUsersSet(std::string fileName) {

  std::set<std::string> strSet;
  std::ifstream infile(fileName.c_str());
  std::string line;
  
  while (std::getline(infile, line)) {
    strSet.insert(line);
  }

  return strSet;
  
}


//reset vertices value after each iteration
void resetVertex(graph_type::vertex_type& vertex) {
  vertex.data().pagerank = 0.0;
  if (vertex.data().userId.compare(START_USER) == 0) {
    vertex.data().pagerank = 1.0;
  }
  vertex.data().counter = 0;
}


int main(int argc, char **argv) {
  graphlab::mpi_tools::init(argc, argv);
  graphlab::distributed_control dc;

  std::string usersFile;
  std::string graphPath;
  int maxIter = 10;

  std::set<std::string> userSet;
  std::set<std::string>::const_iterator userIter;
  
  //main body
  dc.cout() << "Personalized PageRank! \n";
  
  //parse commandline options
  graphlab::command_line_options clopts("Personalized PageRank algorithm");

  clopts.attach_option("graphPath", graphPath, "The graph file. Required ");
  clopts.add_positional("graphPath");
  clopts.attach_option("usersFile", usersFile, "The users file. Required ");
  clopts.add_positional("usersFile");

  clopts.attach_option("maxIter", maxIter, "The max iteration");
  
  if (!clopts.parse(argc, argv)) return EXIT_FAILURE;

  if (!clopts.is_set("graphPath")) {
    std::cout << "input graph path is not provided" << std::endl;
    clopts.print_description();
    return EXIT_FAILURE;
  }

  if (!clopts.is_set("usersFile")) {
    std::cout << "users file path is not provided" << std::endl;
    clopts.print_description();
    return EXIT_FAILURE;
  }

  //set global max iter to the passed max iter
  MAX_ITER = maxIter;
  
  //load the graph from graph.txt*
  //pass the graph in argv
  graph_type graph(dc);
  graph.load(graphPath, lineParser);


  //parse a set or list of nodes, set each of them as start node and
  userSet = getUsersSet(usersFile);

  //create a synchronous engine, to perform GAS in lock step
  graphlab::omni_engine<PersPageRankProg> engine(dc, graph, "sync");


  
  //perform vertex program for each user in the set
  for (userIter = userSet.begin(); userIter != userSet.end(); userIter++) {
    //get the new user
    START_USER = *userIter;

    //reset graph
    graph.transform_vertices(resetVertex);
    
    //signal all vertices to run
    engine.signal_all();
    
    //begin execution of all signalled vertices
    engine.start();
    
    //save the information after applying the page rank iteration
    graph.save(START_USER + "_oput", GraphWriter(), false, true, false);
    
  }
  
  graphlab::mpi_tools::finalize();
  return EXIT_SUCCESS;
}
