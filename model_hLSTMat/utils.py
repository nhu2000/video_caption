import os
import cPickle as pickle
import numpy as np


def decode_captions(captions, idx_to_word):
    if captions.ndim == 1:
        T = captions.shape[0]
        N = 1
    else:
        N, T = captions.shape

    decoded = []
    for i in range(N):
        words = []
        for t in range(T):
            if captions.ndim == 1:
                word = idx_to_word[captions[t]]
            else:
                word = idx_to_word[captions[i, t]]
            if word == '<end>':
                words.append('.')
                break
            if word != '<pad>':
                words.append(word)
        decoded.append(' '.join(words))
    return decoded


def write_bleu(scores, path, epoch):
    if epoch == 0:
        file_mode = 'w'
    else:
        file_mode = 'a'
    with open(os.path.join(path, 'val.bleu.scores.txt'), file_mode) as f:
        f.write('Epoch %d\n' % (epoch + 1))
        f.write('Bleu_1: %f\n' % scores['Bleu_1'])
        f.write('Bleu_2: %f\n' % scores['Bleu_2'])
        f.write('Bleu_3: %f\n' % scores['Bleu_3'])
        f.write('Bleu_4: %f\n' % scores['Bleu_4'])
        f.write('METEOR: %f\n' % scores['METEOR'])
        f.write('ROUGE_L: %f\n' % scores['ROUGE_L'])
        f.write('CIDEr: %f\n\n' % scores['CIDEr'])


def load_pickle(path):
    with open(path, 'rb') as f:
        file = pickle.load(f)
        print ('Loaded %s..' % path)
        return file


def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print ('Saved %s..' % path)


def sample_coco_minibatch(data, batch_size):
    data_size = data['features'].shape[0]
    mask = np.random.choice(data_size, batch_size)
    features = data['features'][mask]
    file_names = data['file_names'][mask]
    return features, file_names
