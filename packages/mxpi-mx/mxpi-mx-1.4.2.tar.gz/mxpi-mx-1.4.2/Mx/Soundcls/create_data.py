import os

# 生成数据列表
def get_data_list(audio_path, list_path):
    sound_sum = 0
    audios = os.listdir(audio_path)
    audioss=[]
    for i in audios:
        if '.txt' not in i :
            audioss.append(i)

    f_train = open(os.path.join(list_path, 'train_list.txt'), 'w', encoding='utf-8')
    f_test = open(os.path.join(list_path, 'test_list.txt'), 'w', encoding='utf-8')
    f_label = open(os.path.join(list_path, 'label_list.txt'), 'w', encoding='utf-8')

    for i in range(len(audioss)):
        f_label.write(f'{audioss[i]}\n')
        sounds = os.listdir(os.path.join(audio_path, audioss[i]))
        for sound in sounds:
            sound_path = os.path.join(audio_path, audioss[i], sound).replace('\\', '/')
            if sound_sum % 100 == 0:
                f_test.write('%s\t%d\n' % (sound_path, i))
            else:
                f_train.write('%s\t%d\n' % (sound_path, i))
            sound_sum += 1
        print("Audio：%d/%d" % (i + 1, len(audioss)))
    f_label.close()
    f_test.close()
    f_train.close()
    return len(audioss)

if __name__ == '__main__':
    get_data_list('sound', '')