# BERT model correct error character with mask feature
实在抱歉,之前做项目比较急,然后没有完全上传完文件,导致大家使用受阻,现已更新  
有人提醒缺少模型，近期空闲，特意将[bert模型](https://pan.baidu.com/s/1VIBfl0wbOIsKaO7FAfR1Zg)奉上,提取码为：hhxx 
另外其中缺少得文件也有上传，安心食用。

# 另 实体识别纠错,ner_for_corrector
实体识别纠错的效果还可以，见[代码](https://github.com/tongchangD/ner_for_corrector),，详情介绍见[地址](https://blog.csdn.net/tcd1112/article/details/107363262)    

## Bert 使用说明

1. 保存预训练模型在data文件夹下
├── data  
│   ├── bert_config.json  
│   ├── config.json  
│   ├── pytorch_model.bin  
│   └── vocab.txt  
├── bert_corrector.py  
├── config.py  
├── logger.py  
├── predict_mask.py  
├── README.md  
└── text_utils.py  

2. 运行`bert_corrector.py`可以进行纠错。
```   
python bert_corrector.py   
```   
3. 运行'predict_mask.py' 可以直接观测用[mask] 掩盖的地方可能出现的汉字    
'''    
python predict_mask.py   
'''   
4. 评估
通用数据下训练的结果并不适用于垂直领域的纠错，需要重新训练  
```   
export CUDA_VISIBLE_DEVICES=0  
python run_lm_finetuning.py \  
    --output_dir=chinese_finetuned_lm \
    --model_type=bert \
    --model_name_or_path=bert-base-chinese \
    --do_train \
    --train_data_file=$TRAIN_FILE \
    --do_eval \
    --eval_data_file=$TEST_FILE \
    --mlm
    --num_train_epochs=3  
```   
      
或者使用  
```   
python -m run_lm_finetuning \  
    --bert_model bert-base-uncased \  
    --do_lower_case \  
    --do_train \ 
    --train_file ./samples/sample_text.txt \  
    --output_dir ./samples/samples_out \  
    --num_train_epochs 5.0 \  
    --learning_rate 3e-5 \  
    --train_batch_size 16 \  
    --max_seq_length 128  
```   
参数可根据机器设备进行删改 
