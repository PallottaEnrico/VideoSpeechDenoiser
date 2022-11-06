import argparse
from pydub import AudioSegment
from math import ceil
import os
from progress.bar import ChargingBar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "noisy_file",
        type=str,
        help="Video to denoise",
    )
    parser.add_argument(
        "-l", "--len",
        required=False,
        type=int,
        default=5,
        help="Length in minutes of each segment of the splitted audio track (5 deafult)",
    )
    parser.add_argument(
        "-o", "--outDir",
        required=False,
        type=str,
        default="",
        help="The directory path where you want to save the new video file (current dir default)",
    )

    args = parser.parse_args()
    inputFile = args.noisy_file
    outDir = args.outDir
    if not os.path.isfile(inputFile):
        print("File not exists")
        exit()

    if inputFile.split(".")[-1] != "mp4":
        print("The file must to be in \'mp4\' format")
        exit()
    splittedName = os.path.basename(inputFile).split(".")[0]
    audioFile = splittedName + ".wav"

    tmpdir = '.videoDenoiser.tmp'
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    else:
        os.system("rm -rf {tmpdir}/*".format(tmpdir=tmpdir))

    print("Extracting audio ...\n")
    status = os.system("ffmpeg -y -i {inputFile} -ac 2 -f wav {tmpdir}/{audioFile} > /dev/null 2>&1".format(inputFile=inputFile, tmpdir=tmpdir, audioFile=audioFile))
    if status != 0:
        print("Problem with audio extraction")
        print("Aborting")
        exit()

    unit = args.len * 60 * 1000 # l minutes in milliseconds
    newAudio = AudioSegment.from_wav(tmpdir + "/" + audioFile)
    tot = len(newAudio)
    n_parts = ceil(tot/unit)

    bar = ChargingBar('Denoising', max=n_parts)
    bar.next(0)
    for i in range(n_parts):
        newAudio[i*unit:(i+1)*unit].export("{tmpdir}/track{i}.wav".format(tmpdir=tmpdir, i=i), format="wav")
        status = os.system('deepFilter {tmpdir}/track{i}.wav -o {tmpdir} > /dev/null 2>&1'.format(tmpdir=tmpdir, i=i))
        if status != 0:
            bar.finish()
            print("This is a memory error, try to reduce the value of \'l\'")
            print("Aborting")
            os.system("rm -rf {tmpdir}".format(tmpdir=tmpdir))
            exit()
        bar.next()
        os.system("rm {tmpdir}/track{i}.wav".format(tmpdir=tmpdir, i=i))
        
    print('\t' + str(bar.elapsed_td))
    bar.finish()
    print("Merging the segments...\n")
    tracks = [AudioSegment.from_wav("{tmpdir}/track{i}_DeepFilterNet2.wav".format(tmpdir=tmpdir, i=i)) for i in range(n_parts)]

    result=AudioSegment.empty()
    for t in tracks: result += t

    audioOutput = tmpdir + "/" + splittedName + "_denoised.wav"
    result.export("{audioOutput}".format(audioOutput=audioOutput), format="wav")
    
    if outDir != "" and (not os.path.isdir(outDir)):
        os.mkdir(outDir)
        if outDir[-1] != '/':
            outDir += '/'
              
    print("Creating the new video...\n")
    status = os.system("ffmpeg -y -i {inputFile} -i {audioOutput} -map 0:v -map 1:a -c:v copy -shortest {outDir}{finalVideo} > /dev/null 2>&1".format(
        inputFile=inputFile, audioOutput=audioOutput, outDir=outDir, finalVideo=splittedName+"_denoised.mp4"
    ))
    if status != 0:
        print("Aborting")
        os.system("rm -rf {tmpdir}".format(tmpdir=tmpdir))
        exit()
        
    os.system("rm -rf {tmpdir}".format(tmpdir=tmpdir))
    print("FINISHED")

if __name__ == '__main__':
    main()