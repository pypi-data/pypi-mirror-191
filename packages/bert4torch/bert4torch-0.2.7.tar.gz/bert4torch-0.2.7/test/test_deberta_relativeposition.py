from bert4torch.layers import RelativePositionsEncodingT5
tmp = RelativePositionsEncodingT5(qlen=512, klen=512, relative_attention_num_buckets=256, is_decoder=False)
print(tmp(10, 10))