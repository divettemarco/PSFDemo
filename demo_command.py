# Divette Marco | UTEP | July 25, 2024
from datetime import datetime
import time
import string
import numpy as np

import librosa
from tabulate import tabulate
import sounddevice as sd
from scipy.io import wavfile

import similarity_finder as sf
import audio_recorder

print('please wait 12s to load...')
# create similarity finder object.
similarity_finder = sf.SimilarityFinder(feature_selection=True)
# to store clip info.
clips = []
# dataset is DRAL until user changes it.
current_dataset = 'DRAL'
# used for user input in playing clips
alpha_list = list(string.ascii_lowercase)
alpha_list.pop(alpha_list.index('d'))
alpha_list.pop(alpha_list.index('o'))
# for playing beep noise between utterances.
beep_file_info = wavfile.read('trans.wav')
# true until user initiates exit from program.
program_active = True
# recording duation is 30s until user changes it.
recording_duration = 30
# set up output device to be laptop speakers.
devices = sd.query_devices()
output_device = -1
laptop_device = -1
volt_device = -1
# if laptop speakers found in index 5, set that as default, store index and store volt device index. change 4 and 5 if device indices are different.
if devices[5]['name'] == 'Speakers (Realtek(R) Audio)': # change 5 if laptop output device has a different index.
    volt_device = 4
    output_device = 5
    sd.default.device = (None, output_device)
    laptop_device = output_device

# will take default device, laptop speakers.
else:
    output_device = sd.default.device[1] # store default output device.
    laptop_device = sd.default.device[1]
    # print(sd.default.device[1])
# to print all devices
# for device in devices:
#     print(device['name'])
#     print(device['index'])
#     print(device['max_output_channels'])
#     # print(device)
# print(sd.default.device)
# quit()

def main():
    # make variables global
    global similarity_finder,clips,current_dataset,program_active,alpha_list,recording_duration,output_device,beep_file_info,devices,volt_device,laptop_device
    # True until user changes it.
    while program_active:
        # print clips if there any.
        if len(clips) > 0:
            display_clips()
            # print play clip menu options for user.
            print('\nplay clips by entering the letter id and one of the following options (ex.a1):\n (1) most similar clip\n (2) 2nd most similar clip\n (3) clip from 3rd quartile\n (4) least similar clip\n')
        # print menu options for user and take input.
        user_input = input(f'choose a menu option:\n (s) start a new recording session\n (r) change recording duration: {recording_duration}s \n (d_) change dataset: {current_dataset} \n\t(d1) DRAL\n\t(d2) ASDNT\n\t(d3) SWBD-MF\n\t(d4) SWBD-M\n\t(d5) SWBD-F\n (o) change output device: {devices[output_device]["name"]} index: {devices[output_device]["index"]}\n (q) quit\n')
        # (s) start a new recording
        if user_input == 's':
            initialize_new_recording_session()
            get_clips()
        # (xx) play clip pair.
        elif len(user_input)==2 and len(clips) > 0 and 'd' not in user_input and 'o' not in user_input:
            try:
                # break down user input and try to play clips.
                clip_choice = alpha_list.index(user_input[0])
                other_clip_choice = int(user_input[1])
                if clip_choice < len(clips) and other_clip_choice < 5 and other_clip_choice > 0:
                    play_clip(clip_choice,other_clip_choice)
                else:
                    print('STET')
            except:
                print('STET')
        # (d) change dataset.
        elif 'd' in user_input and len(user_input) == 2:
            update_dataset(user_input[1])
        # (r) change recording duration.
        elif user_input == 'r':
            # take user input for new recording duration.
            duration_input = input('enter desired duration recording in seconds: \n')
            try:
                recording_duration = int(duration_input)
                print(f'recording duration set as: {recording_duration}')
            except ValueError:
                print('input was not an int. recording duration still set as: ' + str(recording_duration))
        # (o) change device for audio output.
        elif user_input == 'o':
            change_audio_output()
        # (q) quit program.
        elif user_input == 'q':
            program_active = False
            print('quitting...')
        # if user_input was not a menu option.
        else:
            print('STET')

# changes audio output device 
def change_audio_output():
    global devices, output_device, volt_device, laptop_device
    # if volt is not connected keep laptop speakers as output device.
    if volt_device == -1:
        print(f'volt is not connected, audio output device still set as: {devices[output_device]["name"]}')
    # else, it will change output device between laptop speakers and volt.
    elif output_device == volt_device:
        output_device = laptop_device
        sd.default.device = (None, output_device)
        print(f'audio output device set as: {devices[output_device]["name"]}')
        print(f'{devices[output_device]["name"]}')
    elif output_device == laptop_device:
        output_device = volt_device
        sd.default.device = (None, output_device)
        print(f'audio output device set as: {devices[output_device]["name"]}')

# deletes existing clips to start a new recording session.
def initialize_new_recording_session():
    global clips
    clips = []

# prints a table of current clips.
def display_clips():
    global alpha_list, clips, current_dataset
    clip_data = [[alpha_list[x],clips[x]['path'],clips[x]['duration'],clips[x]['dataset'],clips[x]['best_cos'],clips[x]['second_cos'],clips[x]['hundred_cos'],clips[x]['five_hundred_cos']] for x in range(len(clips))]
    print('displaying clips:')
    print(tabulate(clip_data,headers=['id', 'file name', 'duration', 'dataset','1st place','2nd place','third quartile','last place']))

# for ASDNT dataset.
def asd_finder(path):
    global current_dataset
    if current_dataset != 'ASDNT':
        return None
    return 'ASD' if 'ASD-Mono' in path else 'NT'

# updates dataset
def update_dataset(new_dataset):
    global current_dataset
    if new_dataset == '1':
        current_dataset = 'DRAL'
        print('dataset set as: ' + current_dataset)
    elif new_dataset == '2':
        current_dataset = 'ASDNT'
        print('dataset set as: ' + current_dataset)
    elif new_dataset == '3':
        current_dataset = 'SWBD-MF'
        print('dataset set as: ' + current_dataset)
    elif new_dataset == '4':
        current_dataset = 'SWBD-M'
        print('dataset set as: ' + current_dataset)
    elif new_dataset == '5':
        current_dataset = 'SWBD-F'
        print('dataset set as: ' + current_dataset)
    else:
        print('that dataset is not an option, dataset still set as: ' + current_dataset)

# calls the function to find similar and dissimilar clips and stores the clip.
def find_similar_clips(id, path,duration):
    global current_dataset
    first_place, second_place, hundred_place, five_hundred = \
    similarity_finder.find_similar(path, current_dataset)
    clip = {'id': id,
            'path': path[6:],
            'duration': duration,
            'dataset': current_dataset,
            'best_path': first_place[1],
            'best_cos': round(first_place[0].item(), 2),
            'best_asd_label': asd_finder(first_place[1]),
            'second_path': second_place[1],
            'second_cos': round(second_place[0].item(), 2),
            'second_asd_label': asd_finder(second_place[1]),
            'hundred_path': hundred_place[1],
            'hundred_cos': round(hundred_place[0].item(), 2),
            'hundred_asd_label': asd_finder(hundred_place[1]),
            'five_hundred_path': five_hundred[1],
            'five_hundred_cos': round(five_hundred[0].item(), 2),
            'five_hundred_asd_label': asd_finder(five_hundred[1])
            }
    clips.append(clip)

# starts recording, clips utterances, and calls the function to find similar and dissimilar clips.
def get_clips():
    global recording, clips, alpha_list, recording_duration
    input('enter to start recording:')
    print('recording for ' + str(recording_duration) + ' s' )
    start_time = time.time()
    while time.time() - start_time < recording_duration:
        now = datetime.now()
        file_path = f'clips/{now.strftime("%m_%d_%H_%M_%S")}.wav'
        print('file path: ' + file_path)
        audio_recorder.run(file_path)
        clip_id = len(clips) + 1
        duration = librosa.get_duration(path=file_path)
        find_similar_clips(clip_id,file_path,duration)

# will try to play a clip and it's pair clip.
def play_clip(clip_choice, other_choice):
    global beep_file_info
    utt_path = 'clips/' + clips[clip_choice]['path']
    if other_choice == 1:
        other_path = clips[clip_choice]['best_path']
    elif other_choice == 2:
        other_path = clips[clip_choice]['second_path']
    elif other_choice == 3:
        other_path = clips[clip_choice]['hundred_path']
    elif other_choice == 4:
        other_path = clips[clip_choice]['five_hundred_path']
    
    try:
        utt_file_info = wavfile.read(utt_path)
        utt_file_normalized = normalize_audio(utt_file_info[1])
        other_file_info = wavfile.read(other_path)
        other_file_normalized = normalize_audio(other_file_info[1])
        beep_normalized = normalize_audio(beep_file_info[1])
        print(f"playing utterance = {utt_path}")
        sd.play(utt_file_normalized, samplerate=utt_file_info[0])
        sd.wait()
        sd.play(beep_normalized, samplerate=beep_file_info[0])
        sd.wait()
        print(f"playing_path={other_path}")
        sd.play(other_file_normalized, samplerate=other_file_info[0])
        sd.wait()
    except:
        print(f"file path not found when trying to play: {utt_path} or {path}")

# normalizes audio by dividing array representation of audio by max value in array.
def normalize_audio(audio_array):
    max_amplitude = np.max(np.abs(audio_array))
    if max_amplitude > 0:
        return audio_array / max_amplitude
    return audio_array

if __name__ == '__main__':
    main()