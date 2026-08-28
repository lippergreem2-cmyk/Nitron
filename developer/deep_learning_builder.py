import os


class DeepLearningBuilder:

    def create_project(self, name):
        os.makedirs(name, exist_ok=True)

    def write(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)

    # ==========================================
    # Neural Network
    # ==========================================

    def create_neural_network(self):

        self.create_project("neural_network")

        code = '''
import tensorflow as tf

model = tf.keras.Sequential()

print("Neural Network Template")
'''

        self.write("neural_network/main.py", code)

        return "Neural Network project created."
    # ==========================================
    # CNN
    # ==========================================

    def create_cnn(self):

        self.create_project("cnn_model")

        code = '''
import tensorflow as tf

model = tf.keras.Sequential()

print("Convolutional Neural Network Template")
'''

        self.write("cnn_model/main.py", code)

        return "CNN project created."

    # ==========================================
    # RNN
    # ==========================================

    def create_rnn(self):

        self.create_project("rnn_model")

        code = '''
import tensorflow as tf

print("Recurrent Neural Network Template")
'''

        self.write("rnn_model/main.py", code)

        return "RNN project created."

    # ==========================================
    # LSTM
    # ==========================================

    def create_lstm(self):

        self.create_project("lstm_model")

        code = '''
import tensorflow as tf

print("LSTM Template")
'''

        self.write("lstm_model/main.py", code)

        return "LSTM project created."
    # ==========================================
    # Transformer
    # ==========================================

    def create_transformer(self):

        self.create_project("transformer_model")

        code = '''
import tensorflow as tf

print("Transformer Model Template")
'''

        self.write("transformer_model/main.py", code)

        return "Transformer project created."

    # ==========================================
    # GAN
    # ==========================================

    def create_gan(self):

        self.create_project("gan_model")

        code = '''
import tensorflow as tf

print("Generative Adversarial Network Template")
'''

        self.write("gan_model/main.py", code)

        return "GAN project created."

    # ==========================================
    # Autoencoder
    # ==========================================

    def create_autoencoder(self):

        self.create_project("autoencoder_model")

        code = '''
import tensorflow as tf

print("Autoencoder Template")
'''

        self.write("autoencoder_model/main.py", code)

        return "Autoencoder project created."

    # ==========================================
    # Image Classification
    # ==========================================

    def create_image_classifier(self):

        self.create_project("image_classifier")

        code = '''
import tensorflow as tf

print("Image Classification Template")
'''

        self.write("image_classifier/main.py", code)

        return "Image Classification project created."

    # ==========================================
    # Text Classification
    # ==========================================

    def create_text_classifier(self):

        self.create_project("text_classifier")

        code = '''
import tensorflow as tf

print("Text Classification Template")
'''

        self.write("text_classifier/main.py", code)

        return "Text Classification project created."
