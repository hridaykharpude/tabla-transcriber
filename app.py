import gradio as gr
import numpy as np
import pandas as pd
import csv
import librosa
import tensorflow as tf

#!gdown https://drive.google.com/uc?id=1hKQdsTZ35KQmNV9Zrqg-ksTLSmPapR53
model = tf.keras.models.load_model('TTM_model.h5')

def config_audio(audio):
    header = 'ChromaSTFT RMS SpectralCentroid SpectralBandwidth Rolloff ZeroCrossingRate'
    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' label'
    header = header.split()
    file = open('predict_file.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    #taalfile = audio
    #print('stored in taalfile')
    y, sr = librosa.load(audio, mono=True, duration=30)
    rms = librosa.feature.rms(y=y)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    to_append = f' {np.mean(chroma)} {np.mean(rms)} {np.mean(spec_centroid)} {np.mean(spec_bandwidth)} {np.mean(rolloff)} {np.mean(zcr)} '    
    for e in mfcc:
        to_append += f' {np.mean(e)}'
    #to_append += f' {t}'
    file = open('predict_file.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(to_append.split())
    predict_file = pd.read_csv("predict_file.csv")
    X_predict = predict_file.drop('label', axis=1)
    print('exit2')
    return X_predict
    
def predict_audio(Audio_Input):
    audio=Audio_Input.name
    X_predict = config_audio(audio)
    taals = ['addhatrital','bhajani','dadra','deepchandi','ektal','jhaptal','rupak','trital']
    pred = model.predict(X_predict).flatten()
    return {taals[i]: float(pred[i]) for i in range(8)},audio
    
audio = gr.inputs.Audio(source="upload", optional=False)
label = gr.outputs.Label()

audio = gr.inputs.Audio(source="upload", optional=False)
#label = gr.outputs.Label()

gr.Interface(predict_audio, 
            "file",
            [gr.outputs.Label(),gr.outputs.Audio()],
             description="",            
             examples = [["Addhatrital_Sample1.wav"], ["Addhatrital_Sample2.wav"], ["Bhajani_Sample1.wav"], ["Bhajani_Sample2.wav"], 
                         ["Dadra_Sample1.wav"], ["Dadra_Sample2.wav"], ["Deepchandi_Sample1.wav"], ["Deepchandi_Sample2.wav"],
                         ["Ektal_Sample1.wav"], ["Ektal_Sample2.wav"], ["Jhaptal_Sample1.wav"], ["Jhaptal_Sample2.wav"],
                         ["Rupak_Sample1.wav"], ["Rupak_Sample2.wav"], ["Trital_Sample1.wav"], ["Trital_Sample2.wav"]]).launch()
