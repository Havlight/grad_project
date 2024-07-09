from django.shortcuts import render
import io
from PIL import Image as im
from django.views.generic.edit import CreateView
from .models import ImageModel
from .Forms import ImageUploadForm
from ultralytics import YOLO
import os
class UploadImage(CreateView):
    model = ImageModel
    template_name = 'yolo_form.html'
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_instance = form.save(commit=False)
            img_instance.save()
            img = im.open(img_instance.image).convert('RGB')
            # Load YOLOv8 model
            model = YOLO('yolov8s.pt')
            # Perform inference
            results = model(img)
            # 顯示結果
            results[0].show()
            # 保存結果至指定目錄
            save_dir = './media/yolo_out'
            results[0].save(save_dir)  # 保存結果至指定目錄
            # 構建保存圖片的路徑
            inference_img = "./media/yolo_out/" + os.path.basename(results[0].path)
            context = {
                "form": form,
                "inference_img": inference_img
            }
            return render(request, 'yolo_form.html', context)

        context = {
            "form": form
        }
        return render(request, 'yolo_form.html', context)
