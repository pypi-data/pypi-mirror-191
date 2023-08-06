from Mx.Soundcls.macls.predict import PPAClsPredictor
from Mx.Soundcls.macls.utils.record import RecordAudio


class Sound_pre():
    def __init__(self,model_path,record_seconds):
        self.use_gpu=True
        self.record_seconds=record_seconds
        # 读取配置文件
        self.configs={'dataset_conf': {'batch_size': 32, 'num_class': 2, 'num_workers': 4, 'min_duration': 0.1, 'chunk_duration': 1, 'do_vad': False, 'sample_rate': 16000, 'use_dB_normalization': True, 'target_dB': -20, 'train_list': 'train_list.txt', 'test_list': 'test_list.txt', 'label_list_path': 'label_list.txt'}, 'preprocess_conf': {'feature_method': 'MelSpectrogram'}, 'feature_conf': {'sample_rate': 16000, 'n_fft': 1024, 'hop_length': 320, 'win_length': 1024, 'f_min': 50.0, 'f_max': 14000.0, 'n_mels': 64}, 'optimizer_conf': {'learning_rate': 0.001, 'weight_decay': '1e-6'}, 'model_conf': {'embd_dim': 192, 'channels': 512}, 'train_conf': {'max_epoch': 30, 'log_interval': 10}, 'use_model': 'ecapa_tdnn'}
        # 获取识别器
        self.predictor = PPAClsPredictor(configs=self.configs,
                                    model_path=model_path.format(self.configs['use_model'],
                                                                    self.configs['preprocess_conf']['feature_method']),
                                    use_gpu=self.use_gpu)
        self.record_audio = RecordAudio()
    
    def predict(self):
        # 加载数据
        audio_path = self.record_audio.record(record_seconds=self.record_seconds)
        # 获取预测结果
        label, s = self.predictor.predict(audio_path)
        return [label,s]
    
    