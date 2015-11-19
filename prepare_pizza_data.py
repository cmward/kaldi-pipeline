#!/usr/bin/env python
import glob
import sys
import os
import shutil
from subprocess import call, check_output
from os.path import splitext, abspath, basename

"""Script to prepare the pizza order data for Kaldi.

Assumes make_pizza_dir.py has already been run.

Directory format:
    kaldi-pipeline
    |---pizza
        |---steps
        |---utils
        |---test_pizza_audio # test .wav files
        |---train_pizza_audio # train .wav files
        |---data
            |---lang
            |---local
            |   |---dict
            |   |   |---extra_questions.txt
            |   |   |---lexicon.txt
            |   |   |---nonsilence_phones.txt
            |   |   |---optional_silence.txt
            |   |   |---silence_phones.txt
            |   |---lang
            |---test_pizza
            |   |---text
            |   |---utt2spk
            |   |---spk2utt
            |   |---wav.scp
            |---train_pizza
                |---text
                |---utt2spk
                |---spk2utt
                |---wav.scp

NOTE: test_pizza_audio and train_pizza_audio are ignored by github.
"""

KALDI_PATH = os.environ['KALDI']

def downscale(audio_file):
    """If any of the audio files are not 8k, downscale them to be so.
    Downscaled files end with _8k."""
    def is_8k(audio_file):
        check = "sox --i -r {}".format(abspath(audio_file))
        if check_output(check, shell=True).strip() == "8000":
            return True
        else:
            return False
    filename, _ = splitext(basename(audio_file))
    new_name = filename + "_non_8k.wav"
    if not is_8k(audio_file):
        os.rename(audio_file, new_name)
        sox_args = "sox {} {} rate 8000".format(new_name, audio_file)
        call(sox_args, shell=True)
        os.remove(new_name)

def make_text(transcript, text_file):
    """Make the text file in the proper format from the transcript.
    text_file is the location to create the file in."""
    with open(transcript) as text_in:
        with open(text_file, 'w+') as text_out:
            for line in text_in:
                split_line = line.split()
                utt_id = split_line[-1].replace('(', '').replace(')', '')
                speaker_id = utt_id.split('_')[0]
                if "_" not in utt_id:
                    # for files without speaker ids
                    if utt_id.isdigit():
                        speaker_id = "speaker"
                    # speaker name is there, but not separated by underscore
                    else:
                        speaker_id = utt_id.strip('1234567890')
                prefix = speaker_id + "-" + utt_id
                out_line = prefix + " " + " ".join(split_line[:-1]).upper()
                text_out.write(out_line + '\n')

def make_scp(audio_dir, scp_file):
    """Make the .scp file that maps recording ids to audio files.
    scp_file is the location to create the file in."""
    with open(scp_file, 'w+') as scp_file:
        for audio_file in glob.glob(audio_dir+"/*.wav"):
            rec_id = basename(audio_file).split('.')[0]
            scp_line = "{} {}/{}.wav".format(
                rec_id, abspath(audio_dir), rec_id)
            scp_file.write(scp_line + '\n')

def make_utt2spk(text_file, utt2spk_file):
    """Create spk2utt files mapping speaker ids to utt-ids.
    spk2utt file is where it will be created."""
    with open(text_file) as text:
        with open(utt2spk_file, 'w+') as utt2spk:
            for line in text:
                split_line = line.split()
                utt_id = split_line[0]
                spk_id, _ = utt_id.split('-')
                utt2spk_line = "{} {}".format(utt_id, spk_id)
                utt2spk.write(utt2spk_line + '\n')
            utt2spk.write('\n')
                
def main(data_dir):
    ### SORT THESE FILES

    # downscale audio to 8k
    audio_files = (glob.glob('pizza/test_pizza_audio/*.wav') +
                   glob.glob('pizza/train_pizza_audio/*.wav'))
    for audio_file in audio_files:
        downscale(audio_file)

    # make text files
    test_transcript = data_dir + '/devtest/transcript/pizza_devtest'
    train_transcript = data_dir + '/train/transcript/pizza_train'
    make_text(test_transcript, 'pizza/data/test_pizza/text')
    make_text(train_transcript, 'pizza/data/train_pizza/text')

    # make scp files
    test_audio_dir = 'pizza/test_pizza_audio'
    train_audio_dir = 'pizza/train_pizza_audio'
    make_scp(test_audio_dir, 'pizza/data/test_pizza/wav.scp')
    make_scp(train_audio_dir, 'pizza/data/train_pizza/wav.scp')

    # make utt2spk files
    test_text = 'pizza/data/test_pizza/text'
    train_text = 'pizza/data/train_pizza/text'
    make_utt2spk(test_text, 'pizza/data/test_pizza/utt2spk')
    make_utt2spk(train_text, 'pizza/data/train_pizza/utt2spk')

    # make spk2utt files using kaldi util
    test_utt2spk_file = 'pizza/data/test_pizza/utt2spk'
    test_spk2utt_file = 'pizza/data/test_pizza/spk2utt'
    test_args = "{}/egs/wsj/s5/utils/utt2spk_to_spk2utt.pl {} > {}".format(
                KALDI_PATH, test_utt2spk_file, test_spk2utt_file)
    call(test_args, shell=True)

    train_utt2spk_file = 'pizza/data/train_pizza/utt2spk'
    train_spk2utt_file = 'pizza/data/train_pizza/spk2utt'
    train_args = "{}/egs/wsj/s5/utils/utt2spk_to_spk2utt.pl {} > {}".format(
                KALDI_PATH, train_utt2spk_file, train_spk2utt_file)
    call(train_args, shell=True)


