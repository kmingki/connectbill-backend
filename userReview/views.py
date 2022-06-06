from ssl import create_default_context
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from client_commission.models import *

from django.core.exceptions import ImproperlyConfigured

from users.models import DesignerReview, Designer, Message

from .serializers import DesignerReviewSerializer, ReviewSerializer,BriefReviewSerializer,ReviewDetailSerializer

from .models import customerReview
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import numpy as np
import argparse
import imutils
from imutils import paths
import cv2
import math
import os
import shutil
from reborn import settings
from portfolio.models import Projects

MEDIA_ROOT = settings.STATIC_URL
#from .serializer import BriefReviewSerializer


# @api_view(['GET'])
# @permission_classes([AllowAny, ])

    
@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_review(request):
    tmpcommission = Commission.objects.get(id = request.data['commission_id'])
    tmpdesigner = Designer.objects.get(id = tmpcommission.designer.id)
    user = Designer.objects.get(id = tmpcommission.designer.id)

    if request.user.is_client == True and tmpcommission.current_status == 3:
        if request.data['is_panorama'] == 'true' :
            path = request.data.getlist('images')[0]
            # print(image)
        else :
            images = []
            images = request.data.getlist('images')
            os.mkdir(MEDIA_ROOT +'/temp'+str(request.user.id))
            for i in images :
                filename_and_path= MEDIA_ROOT +'/temp'+str(request.user.id)+'/'+ str(i)
                path = default_storage.save(filename_and_path, ContentFile(i.read()))   

            
            print("[INFO] loading images...")
            imagePaths = sorted(list(paths.list_images(MEDIA_ROOT +'/temp'+str(request.user.id))))
            raw_images = []

            for imagePath in imagePaths :
                img= cv2.imread(imagePath)
                img = cv2.resize(img, dsize=(1000, 1000))
                raw_images.append(img)
                
            print("[INFO] switching images...")
            stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
            (tmpstatus, image) = stitcher.stitch(raw_images)
            if tmpstatus == 0:
                path = '/client_committion/committion_image/image.jpg'
                cv2.imwrite(MEDIA_ROOT + path,image)
                cv2.waitKey(0)
                # write the output stitched image to disk

                # display the output stitched image to our screen
                # cv2.imshow("Stitched", image)
                # cv2.waitKey(0)
            else:
                if tmpstatus == cv2.STITCHER_ERR_NEED_MORE_IMGS:
                    print("[INFO] image stitching failed (1: STITCHER_ERR_NEED_MORE_IMGS)")
                    raise Exception("[INFO] image stitching failed (1: STITCHER_ERR_NEED_MORE_IMGS)")
                elif status == cv2.STITCHER_ERR_HOMOGRAPHY_EST_FAIL:
                    print("[INFO] image stitching failed (2: STITCHER_ERR_HOMOGRAPHY_EST_FAIL)")
                    raise Exception("[INFO] image stitching failed (2: STITCHER_ERR_HOMOGRAPHY_EST_FAIL)")        
                else:
                    print("[INFO] image stitching failed (3: STITCHER_ERR_CAMERA_PARAMETERS_ADJUSTMENT_FAIL)")
                    raise Exception("[INFO] image stitching failed (3: STITCHER_ERR_CAMERA_PARAMETERS_ADJUSTMENT_FAIL)")
            shutil.rmtree(MEDIA_ROOT +'/temp'+str(request.user.id))

        client = Client.objects.get(id = request.user.id)
        newReview = customerReview(
            client = client,
            small_image = request.data['small_image'],
            panorama_image = path,
            designer = tmpcommission.designer,
            commission = tmpcommission,
            score = request.data['score'],
            title = tmpcommission.title,
            description=request.data['description'],
        )
        
        newDesignerReview = DesignerReview(
            designer = tmpdesigner,
            review_text = request.data['designer_review'],
            score = request.data['designer_score']
        )
        tmpcommission.current_status = 4

        newMessage = Message(
            user = user,
            message = "'" + str(newReview.title) +"'" + '의뢰에 대한 후기가 작성되었습니다.', 
        )
        tmpPortfolio = DesignerPopol.objects.get(designer = tmpdesigner)

        newProjects = Projects(
            title = tmpcommission.title ,
            small_image = tmpcommission.small_image,
            description = tmpcommission.description,
            participation_data = tmpcommission.finish_date,
            portfolio = tmpPortfolio,
            client = client,
            score = request.data['score']
        )
        
        if not tmpdesigner.average_stars :
            tmpdesigner.average_stars = request.data['score']
        else :
            tmpdesigner.average_stars = tmpdesigner.average_stars + request.data['score']
            tmpdesigner.average_stars = tmpdesigner.average_stars / 2.0
            tmpdesigner.average_stars = round(tmpdesigner.average_stars ,1)

        tmpdesigner.save()
        newProjects.save()
        tmpcommission.save()
        newReview.save()
        newDesignerReview.save()
        newMessage.save()
        return Response(status=status.HTTP_200_OK)
    else :
        return Response(status=status.HTTP_204_NO_CONTENT)
            
@api_view(['GET'])
@permission_classes([AllowAny, ])
def review_view(request) :
    listreview = customerReview.objects.all().order_by('created')
    reviewsSerializer = BriefReviewSerializer(listreview, many= True)
    
    return Response(reviewsSerializer.data, status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def review_view_detail(request,pk):
    review = customerReview.objects.get(id = pk)
    reviewSerializer = ReviewDetailSerializer(review, many=False)

    designerReview = DesignerReview.objects.get(designer = review.designer, commission=review.commission)
    designerReviewSerializer = DesignerReviewSerializer(designerReview,many=False)
   
    return Response({
        'reveiw':  reviewSerializer.data,
        'designer_review' : designerReviewSerializer.data
        }, status=status.HTTP_200_OK)



    
        