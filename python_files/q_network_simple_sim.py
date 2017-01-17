import client_python

class Qnetwork():
    def __init__(self,h_size):

        self.num_actions = 4 # CHANGE
                # INPUTS
        self.drone_x_pos = tf.placeholder(tf.float32, shape=[batch_size], name="drone_x_pos")
        self.drone_z_pos = tf.placeholder(tf.float32, shape=[batch_size], name="drone_y_pos")

        self.drone_x_speed = tf.placeholder(tf.float32, shape=[batch_size], name="drone_x_speed")
        self.drone_z_speed = tf.placeholder(tf.float32, shape=[batch_size], name="drone_z_speed")

        self.target_x = tf.placeholder(tf.float32, shape=[batch_size], name="target_x")
        self.target_z = tf.placeholder(tf.float32, shape=[batch_size], name="target_z")

        self.collided = tf.placeholder(tf.int32, name="collided")

        self.input_size = 6  # will need changing with new network for more complicated task

        self.final_input = tf.concat(1, [drone_x_pos, drone_z_pos, drone_z_speed, drone_z_speed, target_x, target_z])



        # HIDDEN LAYER ONE
        self.hidden_one_units = 5

        self.hidden_one_weights =  tf.Variable(tf.truncated_normal([input_size, hidden_one_units], 
                stddev=1.0 / math.sqrt(float(input_size))),name='hidden_one_weights')

        self.hidden_one_biases = tf.Variable(tf.truncated_normal([hidden_one_units], 
                stddev=1.0 / math.sqrt(float(input_size))),name='hidden_one_biases')

        self.hidden_one = tf.nn.relu(tf.matmul(final_input, hidden_one_weights) + hidden_one_biases)


        # HIDDEN LAYER TWO
        self.hidden_two_units = 5

        self.hidden_two_weights =  tf.Variable(tf.truncated_normal([input_size, hidden_two_units], 
                stddev=1.0 / math.sqrt(float(input_size))),name='hidden_two_weights')

        self.hidden_two_biases = tf.Variable(tf.truncated_normal([hidden_two_units], 
                stddev=1.0 / math.sqrt(float(input_size))),name='hidden_two_biases')

        self.hidden_two = tf.nn.relu(tf.matmul(final_input, hidden_two_weights) + hidden_two_biases)


        # OUTPUT LAYER

        self.weights_op = tf.Variable(tf.truncated_normal([hidden_two_units, num_actions],
                stddev=1.0 / math.sqrt(float(hidden_two_units))), name='weights_op')

        self.q_output = tf.nn.relu(tf.matmul(hidden_two, weights_op))
        
        #Then combine them together to get our final Q-values.
        self.predict = tf.argmax(self.q_output,1) # vector of length batch size
        
        #Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.targetQ = tf.placeholder(shape=[None],dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None],dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions,num_actions,dtype=tf.float32)
        
        self.Q = tf.reduce_sum(tf.mul(self.q_output, self.actions_onehot), reduction_indices=1) # batch size x 1 vector
        
        self.td_error = tf.square(self.targetQ - self.Q)
        self.loss = tf.reduce_mean(self.td_error)
        self.trainer = tf.train.AdamOptimizer(learning_rate=0.0001)
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


def main():
    batch_size = 32 #How many experiences to use for each training step.
    update_freq = 4 #How often to perform a training step.
    y = .99 #Discount factor on the target Q-values
    startE = 1 #Starting chance of random action
    endE = 0.1 #Final chance of random action
    annealing_steps = 10000. #How many steps of training to reduce startE to endE.
    num_episodes = 10000 #How many episodes of game environment to train network with.
    pre_train_steps = 10000 #How many steps of random actions before training begins.
    max_epLength = 1000 #The max allowed length of our episode.
    load_model = False #Whether to load a saved model.
    path = "./dqn" #The path to save our model to.
    tau = 0.001 #Rate to update target network toward primary network
    tf.reset_default_graph()
    mainQN = Qnetwork(h_size)
    targetQN = Qnetwork(h_size)

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
            s = env.reset() # TODO - here, send a reset signal to the simulation
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
                    a = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:[s]})[0]
                s1,r,d = env.step(a) #TODO here, send a message through Imran's server to the simulation
                total_steps += 1
                episodeBuffer.add(np.reshape(np.array([s,a,r,s1,d]),[1,5])) #Save the experience to our episode buffer.
                # TODO ABOVE - make sure you ensure that the reshape idea works correctly
                
                if total_steps > pre_train_steps:
                    if e > endE:
                        e -= stepDrop
                    
                    if total_steps % (update_freq) == 0:
                        trainBatch = myBuffer.sample(batch_size) #Get a random batch of experiences.
                        #Below we perform the Double-DQN update to the target Q-values TODO update the vstack thing
                        actions_from_q1 = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,3])})

                        # TODO below, fix the vstack for trainbatch again
                        Q2 = sess.run(targetQN.Qout,feed_dict={targetQN.scalarInput:np.vstack(trainBatch[:,3])})

                        # todo - wtf is this even doing?
                        end_multiplier = -(trainBatch[:,4] - 1)

                        # todo - i think this is correct, but maybe verify it
                        double_q_value = Q2[range(batch_size),actions_from_q1]
                        targetQ = trainBatch[:,2] + (y*double_q_value * end_multiplier)
                        #Update the network with our target values.
                        _ = sess.run(mainQN.updateModel, \
                            feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,0]),mainQN.targetQ:targetQ, mainQN.actions:trainBatch[:,1]})
                        
                        updateTarget(targetOps,sess) #Set the target network to be equal to the primary network.
                rAll += r
                s = s1
                
                if d == True:
                    break
            
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

    def step_simulation(action):
        client_python.send_message(action)
        client_python.data_received = False
        while not client_python.data_received:
            pass
        cur_state = client_python.data_message
        client_python.data_received = False

