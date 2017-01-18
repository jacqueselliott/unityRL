from client_python import *
import tensorflow as tf
import numpy as np
import math
import os
import random

class Qnetwork():
    def __init__(self):

        self.num_actions = 4 # might CHANGE

        self.input_size = 6  # will need changing with new network for more complicated task

        self.state = tf.placeholder(tf.float32, shape=[None, self.input_size],name="input_state")



        # HIDDEN LAYER ONE
        self.hidden_one_units = 10

        self.hidden_one_weights =  tf.Variable(tf.truncated_normal([self.input_size, self.hidden_one_units], 
                stddev=1.0 / math.sqrt(float(self.input_size))),name='hidden_one_weights')

        self.hidden_one_biases = tf.Variable(tf.truncated_normal([self.hidden_one_units], 
                stddev=1.0 / math.sqrt(float(self.input_size))),name='hidden_one_biases')

        self.hidden_one = tf.nn.relu(tf.matmul(self.state, self.hidden_one_weights) + self.hidden_one_biases)


        # HIDDEN LAYER TWO
        self.hidden_two_units = 10

        self.hidden_two_weights =  tf.Variable(tf.truncated_normal([self.hidden_one_units, self.hidden_two_units], 
                stddev=1.0 / math.sqrt(float(self.input_size))),name='hidden_two_weights')

        self.hidden_two_biases = tf.Variable(tf.truncated_normal([self.hidden_two_units], 
                stddev=1.0 / math.sqrt(float(self.input_size))),name='hidden_two_biases')

        self.hidden_two = tf.nn.relu(tf.matmul(self.hidden_one, self.hidden_two_weights) + self.hidden_two_biases)


        # OUTPUT LAYER

        self.weights_op = tf.Variable(tf.truncated_normal([self.hidden_two_units, self.num_actions],
                stddev=1.0 / math.sqrt(float(self.hidden_two_units))), name='weights_op')

        self.q_output = tf.nn.relu(tf.matmul(self.hidden_two, self.weights_op))
        
        #Then combine them together to get our final Q-values.
        self.predict = tf.argmax(self.q_output,1) # vector of length batch size
        
        #Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.targetQ = tf.placeholder(shape=[None],dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None],dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions,self.num_actions,dtype=tf.float32)
        
        self.Q = tf.reduce_sum(tf.mul(self.q_output, self.actions_onehot), reduction_indices=1) # batch size x 1 vector
        
        self.td_error = tf.square(self.targetQ - self.Q)
        self.loss = tf.reduce_mean(self.td_error)
        self.trainer = tf.train.AdamOptimizer(learning_rate=0.001)
        self.updateModel = self.trainer.minimize(self.loss)


class experience_buffer():
    def __init__(self, buffer_size = 50000):
        self.buffer = []
        self.buffer_size = buffer_size
    
    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)
            
    def sample(self,size):
        return np.reshape(np.array(random.sample(self.buffer,size)),[size,5])



def updateTargetGraph(tfVars,tau):
    total_vars = len(tfVars)
    op_holder = []
    for idx,var in enumerate(tfVars[0:total_vars/2]):
        op_holder.append(tfVars[idx+total_vars/2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars/2].value())))
    return op_holder

def updateTarget(op_holder,sess):
    for op in op_holder:
        sess.run(op)


def main(ws):
    batch_size = 32 #How many experiences to use for each training step.
    update_freq = 4 #How often to perform a training step.
    y = .99 #Discount factor on the target Q-values
    startE = 1 #Starting chance of random action
    endE = 0.1 #Final chance of random action
    annealing_steps = 10000 #How many steps of training to reduce startE to endE.
    num_episodes = 10000 #How many episodes of game environment to train network with.
    pre_train_steps = 1500 #How many steps of random actions before training begins.
    max_epLength = 1500 #The max allowed length of our episode.
    load_model = False #Whether to load a saved model.
    path = "./dqn" #The path to save our model to.
    tau = 0.001 #Rate to update target network toward primary network
    tf.reset_default_graph()
    mainQN = Qnetwork()
    targetQN = Qnetwork()

    init = tf.initialize_all_variables()

    saver = tf.train.Saver()

    trainables = tf.trainable_variables()

    targetOps = updateTargetGraph(trainables,tau)
    myBuffer = experience_buffer()

    #Set the rate of random action decrease. 
    e = startE
    stepDrop = (startE - endE)/annealing_steps

    #create lists to contain total rewards and steps per episode
    rList = []
    jList = []
    total_steps = 0

    #Make a path for our model to be saved in.
    if not os.path.exists(path):
        os.makedirs(path)

    with tf.Session() as sess:
        if load_model == True:
            print 'Loading Model...'
            ckpt = tf.train.get_checkpoint_state(path)
            saver.restore(sess,ckpt.model_checkpoint_path)
        sess.run(init)
        updateTarget(targetOps,sess) #Set the target network to be equal to the primary network.
        for i in range(num_episodes):
            episodeBuffer = experience_buffer()
            # Reset environment and get first new observation
            s = reset(ws)[0] #here, send a reset signal to the simulation
            d = False # TODO check how to use this?
            rAll = 0
            j = 0
            #The Q-Network
            while j < max_epLength: #If the agent takes longer than 1000 moves to finish, end the trial.
                j+=1
                #Choose an action by greedily (with e chance of random action) from the Q-network
                if np.random.rand(1) < e or total_steps < pre_train_steps:
                    a = np.random.randint(0,4)
                else:
                    a = sess.run(mainQN.predict,feed_dict={mainQN.state:[s]})[0]
                s1,r,d = step_simulation(a, ws) # here, send a message through Imran's server to the simulation
                
                total_steps += 1
                episodeBuffer.add(np.reshape(np.array([s,a,r,s1,d]),[1,5])) #Save the experience to our episode buffer.
                # TODO ABOVE - make sure you ensure that the reshape idea works correctly
                
                if total_steps > pre_train_steps:
                    # print "pre reshape"
     
                    
                    # print "post reshape"
                    # print (np.reshape(np.array([s,a,r,s1,d]),[1,5]))
                    print j, rAll
                    if e > endE:
                        e -= stepDrop
                    
                    if total_steps % (update_freq) == 0:
                        trainBatch = myBuffer.sample(batch_size) #Get a random batch of experiences.
                        #Below we perform the Double-DQN update to the target Q-values TODO update the vstack thing
                        actions_from_q1 = sess.run(mainQN.predict,feed_dict={mainQN.state:np.vstack(trainBatch[:,3])})

                        # TODO below, fix the vstack for trainbatch again
                        Q2 = sess.run(targetQN.q_output,feed_dict={targetQN.state:np.vstack(trainBatch[:,3])})

                        # todo - wtf is this even doing?
                        end_multiplier = -(trainBatch[:,4] - 1)

                        # todo - i think this is correct, but maybe verify it
                        double_q_value = Q2[range(batch_size),actions_from_q1]
                        targetQ = trainBatch[:,2] + (y*double_q_value * end_multiplier)
                        #Update the network with our target values.
                        # print (np.shape(trainBatch[:,1]))
                        try:
                            blah = np.vstack(trainBatch[:,0])
                        except:
                            print (trainBatch[:,0])
                        #print ("train batch", trainBatch)
                        _ = sess.run(mainQN.updateModel, \
                            feed_dict={mainQN.state:np.vstack(trainBatch[:,0]),mainQN.targetQ:targetQ, mainQN.actions:trainBatch[:,1]})
                        
                        updateTarget(targetOps,sess) #Set the target network to be equal to the primary network.
                rAll += r
                s = s1
                
                # if d == True:
                #     break
            
            #Get all experiences from this episode and discount their rewards.
            myBuffer.add(episodeBuffer.buffer)
            jList.append(j)
            rList.append(rAll)
            #Periodically save the model. 
            if i % 1000 == 0:
                saver.save(sess,path+'/model-'+str(i)+'.cptk')
                print "Saved Model"
            if len(rList) % 10 == 0:
                print total_steps,np.mean(rList[-10:]), e
        saver.save(sess,path+'/model-'+str(i)+'.cptk')
    print "Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%"

def step_simulation(action, ws):
    action = str(action)
    cur_state = send_message_sync(action, ws)
    return unpack_messages(cur_state)

def calc_reward(drone_pos, target_pos):
    dist = np.linalg.norm(drone_pos-target_pos)
    reward = 0
    if dist > 8*math.sqrt(2):
        reward = -5*(dist-8*math.sqrt(2))/8*math.sqrt(2) 
    if dist < 5*math.sqrt(2):
        reward = +5 - 5*(3*math.sqrt(2) - dist)/3*math.sqrt(2)
    if reward > 1:
        reward =1
    if reward < -0.5:
        reward = -0.5
    return reward

def unpack_messages(msg):
    arr = msg.split(":")
    s = arr[:6]
    s = [float(i) for i in s]
    collison = int(arr[-1])
    done = False
    reward = -2
    if collison == 1:
        print "collision has occurred"
        done = True
        reward = 1000
    else:
        # d_pos = np.array(s[:2])
        # t_pos = np.array(s[4:])
        # reward = calc_reward(d_pos,t_pos)
        reward = 0
    return s, reward, done

def reset(ws):
    return step_simulation(-1, ws)