#include<graphlab.hpp>

/*
 * describe the node i.e user id and its pagerank 
 */
struct User {
  std::string userId;
  double pagerank;
  //initialize user with zero page rank
  User():pagerank(0.0) {}
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
bool lineParser(graph_type& graph, const std::string& fileName,\
		const std::string& textLine) {
  //assign the current line as string stream
  std::stringstream strm(textLine);

  //vertex id of a node
  graphlab::vertex_id vId;

  //userId of the node
  std::string userId;

  //get the user id
  strm >> userId;

  //assign the name as vertex id
  //TODO: check if casting works
  vId = name;

  //insert this node
  graph.add_vertex(vId, User(userId));

  //parse the rest of line to get the other nodes
  while(1) {
    //get other node id of outgoing edge
    graphlab::vertex_id_type otherNodeId;
    strm >> otherNodeId;
    if (strm.fail()) break;
    graph.add_edge(userId, otherNodeId)
  }
}



/*
 * personalized page rank vertex program
 * 
 */
class PersPageRankProg:
  public graphlab::isvertex_program<graph_type, double>,
  public graphlab::IS_POD_TYPE {
  //TODO: figure out the purpose of above directive

private:
  //TODO: how to assign restart probabilities to vertex program from commandline
  //restart probability, 1 - alpha
  double restartProb;

  //rand walk prob, alpha
  double randWalkProb;
  
  //perform gather on all the in-edges
public:
  edge_dir_type gather_edges(icontext_type& context,\
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
  void apply(icontext_type& context, const vertex_type& vertex,\
	     const gather_type& total) {
    //apply the total weighted by random walk prob
    double newRank = randWalkProb * total;
    vertex.data().pagerank = newRank;

    //TODO: check if vertex is start then
    //vertex.data().pagerank = restartProb;
  }

  
  //no scatter needed. return NO_EDGES
  edge_dir_type scatter_edges(icontext_type& context,\
			      const vertex_type& vertex) const {
    return graphlab::NO_EDGES;
  }
  
}


int main(int argc, char **argv) {
  graphlab::mpi_tools::init(argc, argv);
  graphlab::distributed_control dc;

  //main body
  dc.cout() << "Hello World!\n";
  
  //load the graph from graph.txt*
  //TODO: pass the graph in argv
  graph_type graph(dc);
  graph.load("graph.txt", lineParser);

  //create a synchronous engine, to perform GAS in lock step
  graphlab::omni_engine<PersPageRankProg> engine(dc, graph, "sync");

  //signal all vertices to run
  engine.signal_all();

  //begin execution of all signalled vertices
  engine.start();

  graphlab::mpi_tools::finalize();
}
