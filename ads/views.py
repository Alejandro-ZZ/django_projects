from ads.models import Ad, Comment, Fav
from ads.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy, reverse
from ads.forms import CreateForm, CommentForm
from django.db.models import Q
from django.contrib import messages

class AdListView(OwnerListView):
    model = Ad
    # By convention:
    template_name = "ads/ad_list.html"
    def get(self, request) :

        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)

            ad_list = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]

        else:
            ad_list = Ad.objects.all().order_by('-updated_at')

        #Get all id ads with favorite mark
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        ctx = {'ad_list' : ad_list, 'favorites': favorites, 'search': strval}
        return render(request, self.template_name, ctx)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"

    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        # Form is valid
        if form.is_valid():
            posts = Ad.objects.filter(owner__username=self.request.user)
            post_num = posts.count()

            # User have not exceeded number of ads or its me
            if post_num < 3 or str(self.request.user) == 'AlejandroZZ':
                # Add owner to the model before saving
                ad = form.save(commit=False)
                ad.owner = self.request.user
                ad.save()
                return redirect(self.success_url)

            # User EXCEEDED number of ads
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Limit exceeded'})

        # Form is not VALID
        else:
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        form = CommentForm(request.POST)

        # Form is valid
        if form.is_valid():
            posts = Comment.objects.filter(owner__username=self.request.user)
            post_num = posts.count()

            # User have not exceeded number of comments
            if post_num < 5:
                f = get_object_or_404(Ad, id=pk)
                comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
                comment.save()
                return redirect(reverse('ads:ad_detail', args=[pk]))

            # User EXCEEDED number of ads
            else:
                messages.add_message(request, messages.INFO, "Limit exceeded")
                return redirect(reverse('ads:ad_detail', args=[pk]))

        # Form is not VALID
        else:
            messages.add_message(request, messages.ERROR, "Invalid comment")
            return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
