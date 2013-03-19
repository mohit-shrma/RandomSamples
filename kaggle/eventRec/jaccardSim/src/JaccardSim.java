import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.TreeSet;
import java.util.Vector;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import au.com.bytecode.opencsv.CSVReader;



class JaccardSim {
    
    private ArrayList<UserEvents> arrUserEvents;
    
    private enum UserEventsAtn {
        UserInd(0), EventsInd(1);
        private final int ind;
        UserEventsAtn(int ind) {
            this.ind = ind;
        }
        public int index() {
            return ind;
        }
    }
    
    
    private class UserEvents {
        public long user;
        public TreeSet<Long> events;
        public UserEvents(long user, TreeSet<Long> events) {
            this.user = user;
            this.events = events;
        }
        
        
    }
    
    
    private class UserSim {
        long user;
        float sim;
        public UserSim(long user, float sim) {
            this.user = user;
            this.sim = sim;
        }
    }
    
    
    public ArrayList<UserEvents>  prepareArrUserEvents(String eventAttendeesFileName) {
        arrUserEvents = getEventAttendees(eventAttendeesFileName);
        return arrUserEvents;
    }
    
    
    private ArrayList<UserEvents> getEventAttendees(String eventAttendeesFileName) {
        
        ArrayList<UserEvents> userEvents = new ArrayList<UserEvents>();
        
        try {
    
            //read the event attendees file
            CSVReader reader = new CSVReader(new FileReader(eventAttendeesFileName));
    
            String[] nextLine;
            String[] events;
            long user;
            //parse the csv to get event attendees
            while ((nextLine = reader.readNext()) != null) {
                //get the user
                user = Long.parseLong(nextLine[UserEventsAtn.UserInd.index()]);
                //get the events attended by user
                events = nextLine[UserEventsAtn.EventsInd.index()].split("\\s+");
                TreeSet<Long> eventsAttended = new TreeSet<Long>();
                long lEvent = -1;
                for (String event: events) {
                    if (event.length() == 0) {
                        continue;
                    }
                    lEvent = Long.parseLong(event);
                    eventsAttended.add(lEvent);
                }
                //put user and events attended
                userEvents.add(new UserEvents(user, eventsAttended));
            }
            
            reader.close();
            
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
        return userEvents;
    }
    
    
    
    private int getIntersectCount(TreeSet<Long> setA, TreeSet<Long> setB) {
        int intersectCount = 0;
        for (long elem : setA) {
            if (setB.contains(elem)) {
                intersectCount++;
            }
        }
        return intersectCount;
    }

    
    
    //return jaccard similarity with users > userIdx
    private ArrayList<UserSim> getSimUsers(int userIdx) {
        ArrayList<UserSim> simUsers = new ArrayList<UserSim>();
        int numUserEvents = arrUserEvents.size();
        TreeSet<Long> attendedEv = arrUserEvents.get(userIdx).events;
        TreeSet<Long> otherAttendedEv = null;
        int intersectCount, unionCount;
        float jacSim;
        boolean isIntersect;
        for (int i = userIdx + 1; i < numUserEvents; i++) {
            //get the similarity with user 'i'
            otherAttendedEv = arrUserEvents.get(i).events;
            intersectCount = getIntersectCount(attendedEv, otherAttendedEv);
            if (intersectCount > 0) {
                //AUB = A + B -AintersB
                unionCount = attendedEv.size() + otherAttendedEv.size() - intersectCount;
                jacSim = (float)intersectCount/unionCount;
                simUsers.add(new UserSim(arrUserEvents.get(i).user, jacSim));
            }
        }
        return simUsers;
    }
    

    
    private class JaccardSimTask implements Callable<HashMap<Integer, ArrayList<UserSim>>> {
        
        //user index in the userEvents arraylist
        private int userIdx;
        
        public JaccardSimTask(int userIdx) {
            this.userIdx = userIdx;
        }
        
        @Override
        public HashMap<Integer, ArrayList<UserSim>> call() throws Exception {
            HashMap<Integer, ArrayList<UserSim>> result = new HashMap<Integer, ArrayList<UserSim>>();
            //get the user similarities with all users including userIdx+1 
            //and onwards
            ArrayList<UserSim> simUsers = getSimUsers(userIdx);
            result.put(userIdx, simUsers);
            return result;
        }
    }
    
    
    private long getUser(int idx) {
        return arrUserEvents.get(idx).user;
    }
    
    
    private void writeSimilarUsers(HashMap<Integer, ArrayList<UserSim>> simUsers,
                                    FileWriter writer) {
        String user, simUser;
        float jacSim;
        try {
            for (Entry<Integer, ArrayList<UserSim>> entry : simUsers.entrySet())  {
                user = "" + getUser(entry.getKey());
                
                if (entry.getValue().size() == 0) {
                    continue;
                }
                writer.write(user);
                for (UserSim userSim: entry.getValue()) {
                   
                        writer.write(","+userSim.user + ":" + userSim.sim);
                   
                }
                writer.write("\n");
            }
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
    
    
    
    public void findJaccardSimUsersConcurrent(int numThreads, String outputFileName) {
        try {
            //open file to write output
            FileWriter writer = new FileWriter(outputFileName);
            
            ExecutorService threadPool = Executors.newFixedThreadPool(numThreads);
            
            CompletionService<HashMap<Integer, ArrayList<UserSim>>> pool 
                        = new ExecutorCompletionService<HashMap<Integer, ArrayList<UserSim>>>(threadPool);
            
            //get number of tasks or number of similar users
            int numTasks = arrUserEvents.size();
            
            //carry out similarity computation of users
            for (int i = 0; i < numTasks; i++) {
                pool.submit(new JaccardSimTask(i));
            }
            
            HashMap<Integer, ArrayList<UserSim>> simUsers;
            //write results as soon as a task is done
            for (int i = 0; i < numTasks; i++) {
                try {
                    simUsers = pool.take().get();
                    writeSimilarUsers(simUsers, writer);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            writer.close();
            threadPool.shutdown();
        } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        
    }
    
    
    
    public static void main(String[] args) {
        String userEventsFileName = args[0];
        String opFileName = args[1];
        int numThreads = Integer.parseInt(args[2]);
        JaccardSim jacSim = new JaccardSim();
        //read file to make array of user-events pair
        ArrayList<UserEvents> arrUserEvents = 
                jacSim.prepareArrUserEvents(userEventsFileName);
        System.out.println("Number of user events: " + arrUserEvents.size());
        jacSim.findJaccardSimUsersConcurrent(numThreads, opFileName);
    }
    
    
}