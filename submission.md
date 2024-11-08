# Submission document


written by : @chirag chauhan


I went through all the details of the given model, from seamless m4t v1 and v2 to seamless ,I am now capable of fine tuning these models , although only predefined inferences can be fine tuned we can not fine tune an entire engine, i can also deploy this model as a api endpoint and develop a software implementing its use case , although i tried to fine tune this model as well as run few epochs on dummy data, but due to lack of integrated gpu in my system it crashed, thankfully i use linux so i was able to restore my gnome,



in order to deploy this model as an api service we just need to clone this source dir

```bash
git clone https://github.com/facebookresearch/seamless_communication.git
```


and then we can create flask or djnago webapps ,and we can play around as much as we want with different checkpoints from different sections of these seamless models , like seamless expressive , seamless streaming and seamless m4t v - large


the only obstacle in my path is i need a better system to work upon, or a aws instance with good computational power and nice gpu will do just fine


here is the basic colab code for its deployment

```bash
%cd /content
!git clone -b dev https://github.com/camenduru/seamless-m4t-v2-large-hf

!pip install -q fairseq2 gradio
!pip install -q https://huggingface.co/spaces/facebook/seamless-m4t-v2-large/resolve/main/whl/seamless_communication-1.0.0-py3-none-any.whl

!wget https://huggingface.co/spaces/facebook/seamless-m4t-v2-large/resolve/main/assets/sample_input.mp3 -O /content/seamless-m4t-v2-large-hf/assets/sample_input.mp3
!wget https://huggingface.co/spaces/facebook/seamless-m4t-v2-large/resolve/main/assets/sample_input_2.mp3 -O /content/seamless-m4t-v2-large-hf/assets/sample_input_2.mp3

!apt -y install -qq aria2
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/facebook/seamless-m4t-v2-large/resolve/main/seamlessM4T_v2_large.pt -d /content/models -o seamlessM4T_v2_large.pt
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/facebook/seamless-m4t-v2-large/resolve/main/spm_char_lang38_tc.model -d /content/models -o spm_char_lang38_tc.model
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/facebook/seamless-m4t-v2-large/resolve/main/vocoder_v2.pt -d /content/models -o vocoder_v2.pt

%cd /content/seamless-m4t-v2-large-hf
!python app.py
```


[image.png](https://image.png)


This is ofcourse provided by creators and hosted in gradio


i can do just same with custom finetuning, on our own server and use its api, we can do lots of stuff with this , action agents, accessibility models etc etc, possibilities are endless


i have thoroughly understood the structure and fuctioning of this model ie its artitecture.


Thankyou