ARG PYTORCH="2.1.1"
ARG CUDA="12.1.0"
ARG CUDA_SHORT="12.1"
ARG CUDNN="8"
ARG UBUNTU="20.04"

FROM nvidia/cuda:${CUDA}-base-ubuntu${UBUNTU}
FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA_SHORT}-cudnn${CUDNN}-devel

WORKDIR /root/forger/forgeserver
COPY signheredetector /root/forger/signheredetector
COPY signheredetectordataset /root/forger/signheredetectordataset
COPY forgeserver .

COPY forgeserver/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]
