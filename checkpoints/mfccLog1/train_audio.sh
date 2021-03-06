#!/usr/bin/env bash
export CUDA_VISIBLE_DEVICES=0,2
expName=mfccLog1
selfPath=`realpath $0`
cd "$(git rev-parse --show-toplevel)"
mkdir -p checkpoints/$expName/
cp $selfPath checkpoints/$expName/
python train.py \
 --Path "/home/diggerdu/dataset/tfsrc/train/audio/" \
 --additionPath "/home/diggerdu/dataset/tfsrc/extendTrain/" \
 --dumpPath "data/trainDump" \
 --nClasses 12\
 --name $expName --model pix2pix --which_model_netG cnn \
 --nThreads 13\
 --nfft 512 --hop 256 --nFrames 64 --batchSize  3600\
 --split_hop 0 \
 --niter 500 --niter_decay 30 \
 --lr 1e-4 \
 --weightDecay 0 \
 --mixup --mixupAlpha 0.06 \
 --gpu_ids 0,1 \
 --continue_train  --which_epoch 130 \
