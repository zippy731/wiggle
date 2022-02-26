**Wiggle**
---
Generates semirandom keyframes for zoom/spin/translation.  Built for use with Disco Diffusion notebook [link]

Concept: Wiggle is based on the notion of 'episodes' of motion. Each episode is made of three distinct phases: attack (ramp up), decay (ramp down), and sustain (hold level steady).  

Each parameter will ramp UP to a peak during attack phase, will ramp DOWN to a quiet level during decay phase, and will HOLD the quiet level during sustain phase.  

The parameters allow you to set the overall duration of each episode, the time split between phases, and the relative levels of the phases.

Setting | Description | Default
--- | --- | ---
***Time settings***||
max_frames|Total number of frames to model|1000
episode_duration|average duration of each episode, in frames|48
wig_adsmix|time split between attack,decay,sustain periods,should sum to 1.0|(.2,.4,.4)
wig_time_var|allowable variance in time ranges. Must be < 1.0.  Set to 0 for precise control of frames|0.2 
***Zoom settings***||
wig_zoom_range|min/max peak zoom values. Negative values are zoom out.  In DD41, zoom values range around 1.0, so this zoom range is added to 1.0 later|(.12,.18)
wig_zoom_quiet_scale_factor|multiplier factor to reduce zoom peak to zoom 'sustain' level, as function of above range.|.1
***Motion settings***||
wig_angle_range|min/max rotation angle range - max degrees per frame|(-3,3)
wig_trx_range|min/max max pixels of x translation per frame|(-6,6)
wig_try_range|min/max max pixels of y translation per frame|(-6,6)
wig_quiet_scale_factor|multiplier factor to reduce motion vales from peak to lower 'quiet' sustain period|.15

**Typical ADS/ settings:**
Different types of motion can be gained with combinations of the ADS timing and the two quiet scale settings

ADS Settings | WZQS | WQS |  Description 
--- | --- | --- | ---
***ADS tweaks***|||
(.2,.4,.4)| 0.20 | 0.15 |'purposeful' motion, gliding toward destination, pause at destination
(.1,.5,.4)| 0.20 | 0.15 |'sharp' motion, gliding toward destination, pause at destination
(.3,.3,.4)| 0.20 | 0.15 |meandering motion, gently gliding toward destination, pause at destination
***quiet factor tweaks***|||
(.2,.4,.4)| 0.85 | 0.15 |steady zooming, with periodic turns
(.2,.4,.4)| 3.0 | 0.15 |(use with lower base zoom ranges) - sharp turns with minimal zooming, then faster zooming with less turning








#======= WIGGLE MODE
#@markdown ---
#@markdown ####**Wiggle:**
#@markdown Generates semirandom keyframes for zoom / spin / translation. Set params in code.
#@markdown
import random
max_frames = 1000#@param {type:"number"}

wiggle_instead = True 
wiggle_show_params = True 
#if used directly in disco notebook, these sh/b parameterized. Otherwise, just leave them as True.
#wiggle_instead = True #@param {type:"boolean"} 
#wiggle_show_params = True #@param {type:"boolean"} 

if wiggle_instead:
    # make random keyframes within the range of max_frames
    # change every 48 frames or so, with 12 - 36 frame gaps to avoid jerky movements
    # alternating 'episodes' of fast and slow periods.  
    # Fast = zoom/spin/translate, 
    # Slow = quiet pauses with lower values of all tranforme 
    #sequences should be random lengths of 20-30, 20-30, 25-40 frames

    #episode time settings
    episode_duration = 24 # average duration of each episode, in frames
    episode_count = round((max_frames)/(episode_duration*.8),0)
    #attack/decay/sustain mix
    wig_adsmix = (.083,.5,.417) #should sum to 1.0
    wig_time_var = 0.0 # def 0.2 | allowable variance in time ranges. Must be < 1.0.  Set to 0 for precise control of frames.
    #lead_pause = random.randrange(11,13) # frames before first episode
    lead_pause = 12 # number of warmup frames before first episode. Recommended 6-12 to allow image to form before animation starts. 
    
    #calc time ranges    
    wig_attack_range=(round(episode_duration*wig_adsmix[0]*(1-wig_time_var),0),round(episode_duration*wig_adsmix[0]*(1+wig_time_var),0))
    wig_decay_range=(round(episode_duration*wig_adsmix[1]*(1-wig_time_var),0),round(episode_duration*wig_adsmix[1]*(1+wig_time_var),0))
    wig_sustain_range=(round(episode_duration*wig_adsmix[2]*(1-wig_time_var),0),round(episode_duration*wig_adsmix[2]*(1+wig_time_var),0))

    wig_zoom_range=(.12,.18) # max zoom per frame.  Below, we'll add 100% to normalize 
    wig_zoom_quiet_scale_factor = .1 # scale of zoom quiet periods, as function of above range

    wig_angle_range=(-3,3) #rotation angle range - max degrees per frame
    wig_trx_range=(-24,24) #x translation range - pixels per frame
    wig_try_range=(-6,6) #y translation range - pixels per frame
    wig_quiet_scale_factor = .15 # scale of quiet periods, as function of above ranges
    #------------

    episodes = [(0,1.0,0,0,0)] #initialize episodes list
    episode_starts = [0]
    episode_peaks = [0]
    i = 1
    skip_1 = 0
    wig_frame_count = round(lead_pause,0)
    while i < episode_count:
      #attack: quick ramp to motion
      if wig_time_var == 0:
        skip_1 = wig_attack_range[0]
      else:
        skip_1 = round(random.randrange(wig_attack_range[0],wig_attack_range[1]),0)
      wig_frame_count += int(skip_1)
      zoom_1 = 1+round(random.uniform(wig_zoom_range[0],wig_zoom_range[1]),3)
      angle_1 = round(random.uniform(wig_angle_range[0],wig_angle_range[1]),3)
      trx_1 = round(random.uniform(wig_trx_range[0],wig_trx_range[1]),3)
      try_1 = round(random.uniform(wig_try_range[0],wig_try_range[1]),3)
      episodes.append((wig_frame_count,zoom_1,angle_1,trx_1,try_1))
      episode_starts.append((wig_frame_count))
      #decay: ramp down to element of interest
      if wig_time_var == 0:
        skip_1 = wig_decay_range[0]
      else:
        skip_1 = round(random.randrange(wig_decay_range[0],wig_decay_range[1]),0)
      wig_frame_count += int(skip_1)
      zoom_1 = 1+(round(wig_zoom_quiet_scale_factor*random.uniform(wig_zoom_range[0],wig_zoom_range[1]),3))
      angle_1 = round(wig_quiet_scale_factor*random.uniform(wig_angle_range[0],wig_angle_range[1]),3)
      trx_1 = round(wig_quiet_scale_factor*random.uniform(wig_trx_range[0],wig_trx_range[1]),3)
      try_1 = round(wig_quiet_scale_factor*random.uniform(wig_try_range[0],wig_try_range[1]),3)
      episodes.append((wig_frame_count,zoom_1,angle_1,trx_1,try_1))
      episode_peaks.append((wig_frame_count))
      #sustain: pause during element of interest
      if wig_time_var == 0:
        skip_1 = wig_sustain_range[0]
      else:
        skip_1 = round(random.randrange(wig_sustain_range[0],wig_sustain_range[1]),0)
      wig_frame_count += int(skip_1)
      zoom_1 = 1+(round(wig_zoom_quiet_scale_factor*random.uniform(wig_zoom_range[0],wig_zoom_range[1]),3))
      angle_1 = round(wig_quiet_scale_factor*random.uniform(wig_angle_range[0],wig_angle_range[1]),3)
      trx_1 = round(wig_quiet_scale_factor*random.uniform(wig_trx_range[0],wig_trx_range[1]),3)
      try_1 = round(wig_quiet_scale_factor*random.uniform(wig_try_range[0],wig_try_range[1]),3)
      episodes.append((wig_frame_count,zoom_1,angle_1,trx_1,try_1))
      i+=1
    #trim off any episode > max_frames
    cleaned_episodes = [i for i in episodes if i[0] < max_frames]
    episodes = cleaned_episodes
    cleaned_episode_starts = [i for i in episode_starts if i < max_frames]
    episode_starts = cleaned_episode_starts
    cleaned_episode_peaks = [i for i in episode_peaks if i < max_frames]
    episode_peaks = cleaned_episode_peaks

    #build full schedule
    keyframe_frames = [item[0] for item in episodes]
    #print('keyframe_frames is ')
    #print(keyframe_frames)
    wig_goalschedule=[(1,1,0,0,0)] # initial frame in the full schedule
    i=1  # skip first frame, already set above
    while i < max_frames: 
      if(i+1 in keyframe_frames):
        zoomgoal = episodes[keyframe_frames.index(i+1)][1]
        anglegoal = episodes[keyframe_frames.index(i+1)][2]
        trxgoal = episodes[keyframe_frames.index(i+1)][3]
        trygoal = episodes[keyframe_frames.index(i+1)][4]
      else:
        zoomgoal = wig_goalschedule[i-1][1]
        anglegoal = wig_goalschedule[i-1][2]
        trxgoal = wig_goalschedule[i-1][3]
        trygoal = wig_goalschedule[i-1][4]
      wig_goalschedule.append((i,zoomgoal,anglegoal,trxgoal,trygoal))
      #print('wig_goalschedule midloop is ')
      #print(wig_goalschedule)
      i += 1
    #print('wig_goalschedule is ')
    #print(wig_goalschedule)

    #only plot when testing.
    #plotx=[]
    #ploty=[]#zoom goals
    #ploty2=[]#zoom actual
    #ploty3=[]#exit inertia
    #ploty4=[]#zoom_pow_tgt
    #ploty5=[]#zoompowactual

    wig_zoom_goals = [goal[1] for goal in wig_goalschedule]
    wig_angle_goals = [goal[2] for goal in wig_goalschedule]
    wig_trx_goals = [goal[3] for goal in wig_goalschedule]
    wig_try_goals = [goal[4] for goal in wig_goalschedule]
    #print('wig_zoom_goals is ')
    #print(wig_zoom_goals)

    #Build keyframe strings 
    wig_zoom_string=''
    wig_angle_string=''
    wig_trx_string=''
    wig_try_string=''
    # iterate thru episodes, generate keyframe strings
    ### reformat as keyframe strings for testing
    i = 0
    while i < len(episodes):
      wig_zoom_string += str(int(episodes[i][0]))+':('+str(episodes[i][1])+'),'
      wig_angle_string += str(round(episodes[i][0],0))+':('+str(episodes[i][2])+'),'
      wig_trx_string += str(round(episodes[i][0],0))+':('+str(episodes[i][3])+'),'
      wig_try_string += str(round(episodes[i][0],0))+':('+str(episodes[i][4])+'),'
      i+=1
    

    zoom = wig_zoom_string
    angle = wig_angle_string 
    translation_x = wig_trx_string
    translation_y =  wig_try_string
    if wiggle_show_params:
      print('keyframe transitions:')
      print(keyframe_frames)
      print('episode_starts:')
      print(episode_starts)
      print('episode_peaks:')
      print(episode_peaks)
      print ('angle is')
      print(angle)    
      print ('zoom is')
      print(zoom)
      print ('translation_x is')
      print(translation_x)
      print ('translation_y is')
      print(translation_y)  
      print('end of wiggle params')

#plotter for testing    
#    from matplotlib import pyplot as plt 
#    plt.subplot(3, 1, 1)
#    import matplotlib.pyplot as plt
#    plt.rcParams["figure.figsize"] = (20,12)
#    plt.plot(plotx, ploty) 
#    plt.plot(plotx, ploty2)
#    plt.title('Tgt and Actual Value')  
#    plt.subplot(3, 1, 2) 
#    plt.title('Exit Inertia') 
#    plt.plot(plotx, ploty3)
#    plt.subplot(3, 1, 3) 
#    plt.title('Tgt and Actual Power') 
#    plt.plot(plotx, ploty4)
#    plt.plot(plotx, ploty5)
#    plt.show()     

#============= END WIGGLE
