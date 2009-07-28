from pyfann import libfann
def create_and_train_ann(train_file, target_file="./default.train"):
  num_input = 250
  num_output = 1
  num_layers = 3
  num_neurons_hidden = 10
  desired_error = 0.0001
  max_epochs = 5000
  epochs_between_reports = 1000
  max_neurons = 100
  neurons_between_reports = 1
  steepnesses = [0.1,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]


  #Training the ann
  train_data = libfann.training_data()
  train_data.read_train_from_file(train_file)

  train_data.scale_train_data(0,1)
  
  # Create the ann
  ann = libfann.neural_net()
  ann.create_shortcut_array([len(train_data.get_input()[0]), len(train_data.get_output()[0])])
  
  #Configuring the net
  ann.set_training_algorithm(libfann.TRAIN_RPROP)
  ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC)
  ann.set_activation_function_output(libfann.LINEAR_PIECE)
  ann.set_train_error_function(libfann.ERRORFUNC_LINEAR)
  ann.set_rprop_increase_factor(1.2)
  ann.set_rprop_decrease_factor(0.5)
  ann.set_rprop_delta_min(0.0)
  ann.set_rprop_delta_max(50.0)
  ann.set_cascade_output_change_fraction(0.01)
  ann.set_cascade_output_stagnation_epochs(12)
  ann.set_cascade_candidate_change_fraction(0.01)
  ann.set_cascade_candidate_stagnation_epochs(12)
  ann.set_cascade_weight_multiplier(0.4)
  ann.set_cascade_candidate_limit(1000.0)
  ann.set_cascade_max_out_epochs(max_epochs)
  ann.set_cascade_max_cand_epochs(150)
  ann.set_cascade_activation_steepnesses(steepnesses)
  ann.set_cascade_num_candidate_groups(1)
  
  #Printing a piece of information about the net
  ann.print_parameters()
   
#  ann.cascadetrain_on_data(train_data, max_neurons, neurons_between_reports, desired_error)
  
  ann.print_connections()
   
  ann = libfann.neural_net()

  #Actually, i don't know what it is.
  ann.create_shortcut_array([len(train_data.get_input()[0]), len(train_data.get_output()[0])])
  
  
  ann.print_parameters()
 
  #Training the net
  ann.cascadetrain_on_data(train_data, max_neurons, neurons_between_reports, desired_error)
  
  ann.print_connections()

  ann.save(target_file)

def load_and_run_ann(net_file, input):
  if net_file != None:
    ann = libfann.neural_net()
    ann.create_from_file(net_file)
    result = ann.run(input)
    print " Ann test New Pattern, result is: %s"%str(result)
    return result

def load(net_file):
  if net_file != None:
    ann = libfann.neural_net()
    ann.create_from_file(net_file)
    return ann
  else:
    raise AttributeError, "File path does not exist."


if __name__ == '__main__':
  import util
  from horus.core.processingimage import image 
  #create_and_train_ann('./default.train', './ann.net')
  img = image.Image(path='/tmp/train/esquerdaNova.png')                              
  input = util.get_pattern_from_image(img)
  print "input --------------------------------%s"%str(input)
  load_and_run_ann('./ann.net', input)
  

