from rest_framework.generics import RetrieveAPIView

from userprofile.apis.serializers import SellerSerializer
from userprofile.models import Seller


class SellerDetailView(RetrieveAPIView):
    serializer_class = SellerSerializer

    def get_object(self):
        return Seller.objects.get(pk=self.kwargs['pk'])