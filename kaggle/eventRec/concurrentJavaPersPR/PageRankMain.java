import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.PreparedStatement;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeSet;
import java.util.Vector;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.commons.lang3.StringUtils;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;
import java.lang.Math;


class PageRankMain {
    
    private HashMap<Long, Vector<Long>> adjList;
    private int maxIter;
    
    PageRankMain(int maxIter) {
        this.maxIter = maxIter;
    }
    
    private enum PageRankConsts {
        MaxIter(100), Alpha(0.5), TopNum(100), Eps(0.000001);
        private final double val;
        PageRankConsts(double val) {
            this.val = val;
        }
        public double val() {
            return val;
        }
    }
    
    private enum Friends {
        UserInd(0), FriendsInd(1);
        private final int ind;
        Friends(int ind) {
            this.ind = ind;
        }
        public int index() {
            return ind;
        }
    }
    
    private enum TrainConsts {
        UserInd(0);
        private final int ind;
        TrainConsts(int ind) {
            this.ind = ind;
        }
        public int index() {
            return ind;
        }
    }
    
    private enum TestConsts {
        UserInd(0);
        private final int ind;
        TestConsts(int ind) {
            this.ind = ind;
        }
        public int index() {
            return ind;
        }
    }
    

    private class PageRankTask implements Callable<HashMap<Long, ArrayList<Long>>> {

        private long node;
        
        public PageRankTask(long user) {
            this.node = user;
        }
        
        @Override
        public HashMap<Long, ArrayList<Long>> call() throws Exception {
            HashMap<Long, ArrayList<Long>> result= new HashMap<Long, ArrayList<Long>>();
            ArrayList<Long> topUsers = topPRUsers(node);
            result.put(node, topUsers);
            return result;
        }
        
    }
    
    
    private TreeSet<Long> getUserSet(String fileName) {
        
        TreeSet<Long> set = new TreeSet<Long>(); 
        
        try {
            
            //read the users file
            CSVReader reader = new CSVReader(new FileReader(fileName));
            
            //skip header
            reader.readNext();
            
            String[] nextLine;
            long user;
            //parse the csv to get the user
            while ((nextLine = reader.readNext()) != null) {
                //get the user
                if ((nextLine[Friends.UserInd.index()]).length() > 0) {
                    user = Long.parseLong(nextLine[Friends.UserInd.index()]);
                    set.add(user);
                }
            }
            
            reader.close();
            
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
        return set;
        
    }
    
    
    public HashMap<Long, Vector<Long>> prepAdjList(String friendsFileName,
                                                          Set<Long> trainSet,
                                                          Set<Long> testSet) {
        
        HashMap<Long, Vector<Long>> adjList = new HashMap<Long, Vector<Long>>();
        
        try {
            
            //read the friends file
            CSVReader reader = new CSVReader(new FileReader(friendsFileName));
            
            //skip header
            reader.readNext();
            
            String[] nextLine;
            long user  = -1;
            
            
            //parse the csv to get the user and friends
            while ((nextLine = reader.readNext()) != null) {
                //get the user
                if (nextLine[Friends.UserInd.index()].length() > 0) {
                    user = Long.parseLong(nextLine[Friends.UserInd.index()]);
                    //get user's friends
                    String[] allFriends = nextLine[Friends.FriendsInd.index()].split("\\s+");
                    Vector<Long> friends = new Vector<Long>();
                    long lFriend = -1;
                    for (String friend: allFriends) {
                        if (friend.length() == 0) {
                            continue;
                        }
                        lFriend = Long.parseLong(friend);
                        if (!adjList.containsKey(lFriend)) {
                            adjList.put(lFriend, new Vector<Long>());
                        }
                        friends.addElement(lFriend);
                    }
                    //put the user and his friends
                    adjList.put(user, friends);
                }
            }
            
            reader.close();
            
            //parse the train user, for user with no friends
            for (Long trainUser: trainSet) {
                if (!adjList.containsKey(trainUser)) {
                    adjList.put(trainUser, new Vector<Long>());
                }
            }
            
            //parse the test users, for user with no friends
            for (Long testUser: testSet) {
                if (!adjList.containsKey(testUser)) {
                    adjList.put(testUser, new Vector<Long>());
                }
            }
          
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        this.adjList = adjList;
        return adjList;
    }
    
    private Set<Long> prepareUserSet(String fileName) {
        
        HashSet<Long> userSet = new HashSet<Long>();
        
        //read the friends file
        try {
            CSVReader reader = new CSVReader(new FileReader(fileName));
            
            //skip header
            reader.readNext();
            
            String[] nextLine;
            long user = -1;
            //parse the csv to get the user
            while ((nextLine = reader.readNext()) != null) {
                if (nextLine[Friends.UserInd.index()].length() > 0) {
                    //get the user
                    user = Long.parseLong(nextLine[Friends.UserInd.index()]);
                    userSet.add(user);
                }
            }
            
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
         // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return userSet;
    }
    
    //compute personalized page rank at node, return top nodes
    private ArrayList<Long> topPRUsers(long node) {
        
        //map to hold prob of jumping to node till curr Iteration 
        HashMap<Long, Double>  probs = new HashMap<Long, Double>();
        
        //map to store calculated pagerank probs 
        HashMap<Long, Double>  pageRankProbs = new HashMap<Long, Double>();
        
        //start at current user
        probs.put(node, 1.0);
       
        
        //num of iteration - 3
        //alpha = 0.5
        pageRankProbs = pageRankHelper(node, probs, (int) PageRankConsts.MaxIter.val, 
                                        PageRankConsts.Alpha.val);
       
        //get the top keys with highest page rank except the current node
        //remove cuurent user from page ranks
        pageRankProbs.remove(node);
        
        //sort the map by values
        pageRankProbs = (HashMap<Long, Double>) sortByComparator(pageRankProbs);
        
        //get the first top keys
        ArrayList<Long> topSimUsers = new ArrayList<Long>((int) PageRankConsts.TopNum.val);
        int count = 0;
        for (Long key : pageRankProbs.keySet()) {
            if (count >= (int) PageRankConsts.TopNum.val) {
                break;
            }
            topSimUsers.add(0, key);
            count++;
        }
        
        return topSimUsers;
    }
    
    
    /*
     * return a sorted map by value
     */
    private Map sortByComparator(Map unsortMap) {
        List list = new LinkedList(unsortMap.entrySet());
        
        // sort list based on comparator
        Collections.sort(list, new Comparator() {
            public int compare(Object o1, Object o2) {
                return ((Comparable) ((Map.Entry) (o1)).getValue())
                                       .compareTo(((Map.Entry) (o2)).getValue());
            }
        });
 
        // put sorted list into map again
        //LinkedHashMap make sure order in which keys were inserted
        Map sortedMap = new LinkedHashMap();
        for (Iterator it = list.iterator(); it.hasNext();) {
            Map.Entry entry = (Map.Entry) it.next();
            sortedMap.put(entry.getKey(), entry.getValue());
        }
        return sortedMap;
    }
    
    /*
     * start - node to calculate page rank around
     * probs - prob of staying at start of current iteration
     * numIter - number of iterations remaining
     * alpha = probability to walk on neighbor, 
     * i.e. 1-alpha is prob to go back to start
     */
    private HashMap<Long, Double> pageRankHelper(long node2, 
                                                    HashMap<Long, Double> probs,
                                                    int numIter, double alpha) {
        if (numIter <= 0) {
            System.out.println("Iterations: " + numIter);
            return probs;
        } else {
            //map to hold updated probs after this iteration
            HashMap<Long, Double> probsPropagated 
                                            = new HashMap<Long, Double>();
            probsPropagated.put(node2, 1-alpha);
            
            //propagate previous probabilities for each node in it
            for (Entry<Long, Double> entry: probs.entrySet()) {
                Long node = entry.getKey();
                Double prob = entry.getValue();
                Vector<Long> friends = adjList.get(node);
                //move to neighbor with probability alpha
                //distribute each node's probability equally to each neighbor
                if (friends.size() > 0) {
                    double prob2Propagate = alpha * (prob/friends.size());
                    for (Long friend: friends) {
                        if (!probsPropagated.containsKey(friend)) {
                            probsPropagated.put(friend, 0.0);
                        }
                        probsPropagated.put(friend, 
                                probsPropagated.get(friend) + prob2Propagate);
                    }
                }
                
            }
            
            //check for convergence, minError or difference b/w old and new 
            //should be < eps
            double maxError = 0;
            for (Entry<Long, Double> entry: probsPropagated.entrySet()) {
                Long node = entry.getKey();
                Double newProb = entry.getValue();
                if (probs.containsKey(node)) {
                    //older probability present corresponding to this node
                    double diff = Math.abs(probs.get(node) - 
                                                    probsPropagated.get(node));
                    if (diff > maxError) {
                        maxError = diff;
                    }
                } else {
                    //it's a completely new entry
                    //we have to proceed at least till all of them are found
                    maxError = 1;
                    break;
                }
            }
            
            if (maxError < PageRankConsts.Eps.val) {
                //convergence condition met
                System.out.println("Iterations: " + numIter);
                return probsPropagated;
            }
            
            //can delete previous dic we dont need it
            probs.clear();
            
            //recusively propagate pagge rank prob
            return pageRankHelper(node2, probsPropagated, numIter - 1, alpha);
        }
    }
    
    //write the computed similar users to specified file
    public void writeSimUsers(String fileName, 
            HashMap<Long, ArrayList<Long>> simUsers) {
            
        try {
            FileWriter writer = new FileWriter(fileName);
            String user = null;
            //StringBuffer neighbors = new StringBuffer();
            String strNeighbors = null;
            String[] writerArr = new String[2];
            ArrayList<Long> neighbors = null;
            
            for (Entry<Long, ArrayList<Long>> entry: simUsers.entrySet()) {
                //neighbors.delete(0, neighbors.length());
                strNeighbors = null;
                user = "" + entry.getKey();
                neighbors = entry.getValue();
                strNeighbors = StringUtils.join(neighbors, " ");
                writer.write(user + "," + strNeighbors + '\n');
            }
            writer.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
    
    
    public HashMap<Long, ArrayList<Long>> findTopPRUsers(Set<Long> users) {
        
        //get number of tasks
        int numTasks = users.size();
        
        //hashmap to store top similar users
        HashMap<Long, ArrayList<Long>> topSimUsers = 
                new HashMap<Long, ArrayList<Long>>(numTasks);
        
        for (Long user: users) {
            ArrayList<Long> topPRUsers = topPRUsers(user);
            topSimUsers.put(user, topPRUsers);
            //System.out.println( user + " : "+ topPRUsers.toString());
        }
        
        return topSimUsers;
    }
    
    
    public HashMap<Long, ArrayList<Long>> findTopPRUsersConcurrent(Set<Long> users, int numThreads) {
        ExecutorService threadPool = Executors.newFixedThreadPool(numThreads);
        CompletionService<HashMap<Long, ArrayList<Long>>> pool = 
                new ExecutorCompletionService<HashMap<Long, ArrayList<Long>>>(threadPool);
        
        //get number of tasks
        int numTasks = users.size();
        
        //hashmap to store top similar users
        HashMap<Long, ArrayList<Long>> topSimUsers = 
                new HashMap<Long, ArrayList<Long>>(numTasks);
        
        //carry out page rank computation of individual nodes
        for (long user: users) {
            pool.submit(new PageRankTask(user));
        }
        
        //wait for the results of tasks
        for (int i = 0; i < numTasks; i++) {
            try {
                HashMap<Long, ArrayList<Long>> taskResult = pool.take().get();
                for (Entry<Long, ArrayList<Long>> entry: taskResult.entrySet()) {
                    topSimUsers.put(entry.getKey(), entry.getValue());
                }
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (ExecutionException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }
        
        threadPool.shutdown();
        
        return topSimUsers;
    }
    
    
    public static void main(String[] args) {
        
        String trainFileName = args[0];
        String testFileName = args[1];
        String userFriendsFileName = args[2];
        
        String trainSimUsersOp = args[3];
        String testSimUsersOp = args[4];
        int numThreads = Integer.parseInt(args[5]);
        int maxIter = Integer.parseInt(args[6]);
        
        PageRankMain prMain = new PageRankMain(maxIter);
        Set<Long> trainSet = prMain.getUserSet(trainFileName);
        Set<Long> testSet = prMain.getUserSet(testFileName);
        HashMap<Long, Vector<Long>> adjList = 
                prMain.prepAdjList(userFriendsFileName, trainSet, testSet);
        
        //HashMap<Long, ArrayList<Long>>  topSimUsers= prMain.findTopPRUsers(trainSet);
        HashMap<Long, ArrayList<Long>>  topSimUsers = prMain.findTopPRUsersConcurrent(trainSet, numThreads);
        prMain.writeSimUsers(trainSimUsersOp, topSimUsers);
        
        topSimUsers= prMain.findTopPRUsersConcurrent(testSet, numThreads);
        prMain.writeSimUsers(testSimUsersOp, topSimUsers);
    }
    
}