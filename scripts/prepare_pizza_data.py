#!/usr/bin/env python
import glob
import sys
import os
import shutil
from subprocess import call, check_output
from os.path import splitext, abspath, basename
from os.path import join as pjoin
from path import *

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
	    |	|---reco2file_and_channel
	    |	|---segments
            |---train_pizza
                |---text
                |---utt2spk
                |---spk2utt
                |---wav.scp
		|---reco2file_and_channel
		|---segments
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
                out_line = prefix + " " + " ".join(split_line[:-1]).lower()
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

def make_reco2file(audio_dir, reco2file):
    """Make the reco2file_and_channel file
    map recording-id filename recording side"""
    with open(reco2file, 'w+') as reco2file:
        for audio_file in glob.glob(audio_dir+"/*.wav"):
            rec_id = basename(audio_file).split('.')[0]
            reco_line = "{} {} {}".format(rec_id, rec_id, "A")
            reco2file.write(reco_line + '\n')

def make_segments(audio_dir, seg_file):
    """Make segments file, utterance-id = same as text/utt2spk file
    use sox to get end time information (utt-id rec-id utterance start,end"""
    with open(seg_file, 'w+') as seg_file:
        for audio_file in glob.glob(audio_dir+"/*.wav"):
            rec_id = basename(audio_file).split('.')[0]
            if rec_id.isdigit():
                utt_id = "{}-{}".format("speaker", rec_id)
            else:
                utt_id = rec_id
            end_cmd = "sox --i -D {}".format(audio_file).strip()
            end_time = check_output(end_cmd, shell=True)
            seg_line = "{} {} 0.00 {}".format(utt_id, rec_id, end_time).strip()
            seg_file.write(seg_line + '\n')

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
                
def main(data_dir):
    # downscale audio to 8k
    audio_files = (glob.glob('pizza/test_pizza_audio/*.wav') +
                   glob.glob('pizza/train_pizza_audio/*.wav'))
    for audio_file in audio_files:
        downscale(audio_file)

    # make text files
    test_transcript = pjoin(data_dir, 'devtest/transcript/pizza_devtest')
    train_transcript = pjoin(data_dir, 'train/transcript/pizza_train')
    make_text(test_transcript, pjoin(PIZZA_DATA_TE, 'text'))
    make_text(train_transcript, pjoin(PIZZA_DATA_TR, 'text'))

    # make scp files
    make_scp(PIZZA_WAV_TE, pjoin(PIZZA_DATA_TE, 'wav.scp'))
    make_scp(PIZZA_WAV_TR, pjoin(PIZZA_DATA_TR, 'wav.scp'))

    #make reco2file_and_channel files
    make_reco2file(PIZZA_WAV_TE, pjoin(PIZZA_DATA_TE, 'reco2file_and_channel'))
    make_reco2file(PIZZA_WAV_TR, pjoin(PIZZA_DATA_TR, 'reco2file_and_channel'))

    #make segment files
    make_segments(PIZZA_WAV_TE, pjoin(PIZZA_DATA_TE, 'segments'))
    make_segments(PIZZA_WAV_TR, pjoin(PIZZA_DATA_TR, 'segments'))

    # make utt2spk files
    test_text = pjoin(PIZZA_DATA_TE, 'text')
    train_text = pjoin(PIZZA_DATA_TR, 'text')
    make_utt2spk(test_text, pjoin(PIZZA_DATA_TE, 'utt2spk'))
    make_utt2spk(train_text, pjoin(PIZZA_DATA_TR, 'utt2spk'))

    # make spk2utt files using kaldi util
    test_utt2spk_file = pjoin(PIZZA_DATA_TE, 'utt2spk')
    test_spk2utt_file = pjoin(PIZZA_DATA_TE, 'spk2utt')
    test_args = "{} {} > {}".format(
        pjoin(PIZZA_DIR,'utils','utt2spk_to_spk2utt.pl'),
        test_utt2spk_file, test_spk2utt_file)
    call(test_args, shell=True)

    train_utt2spk_file = pjoin(PIZZA_DATA_TR, 'utt2spk')
    train_spk2utt_file = pjoin(PIZZA_DATA_TR, 'spk2utt')
    train_args = "{} {} > {}".format(
        pjoin(PIZZA_DIR,'utils','utt2spk_to_spk2utt.pl'),
        train_utt2spk_file, train_spk2utt_file)
    call(train_args, shell=True)

    #Sort files
    files = glob.glob(PIZZA_DATA_TE+'/*') + glob.glob(PIZZA_DATA_TR+'/*')
    for file in files:
        call("sort {} -o {}".format(file, file),shell=True)
