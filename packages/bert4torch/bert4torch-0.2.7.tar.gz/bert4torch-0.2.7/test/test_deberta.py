from transformers import AutoModelForMaskedLM, AutoTokenizer, FillMaskPipeline
import torch

tokenizer=AutoTokenizer.from_pretrained('F:\Projects\pretrain_ckpt\deberta\[IDEA-CCNL-torch]--Erlangshen-DeBERTa-v2-320M-Chinese', use_fast=False)
model=AutoModelForMaskedLM.from_pretrained('F:\Projects\pretrain_ckpt\deberta\[IDEA-CCNL-torch]--Erlangshen-DeBERTa-v2-320M-Chinese')
text = '生活的真谛是[MASK]。'
fillmask_pipe = FillMaskPipeline(model, tokenizer, device=0)
print(fillmask_pipe(text, top_k=10))
