from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead
from .forms import AddCommentForm,AddLeadForm
from django.urls import reverse_lazy
from django.contrib import messages
from client.models import Client, Comment as ClientComment
from team.models import Team
from django.views.generic import ListView,DetailView,DeleteView,UpdateView,CreateView,View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import add_message, INFO
# Create your views here.

class LeadListView(LoginRequiredMixin,ListView):
    model = Lead

    def get_queryset(self):
        queryset = super(LeadListView,self).get_queryset()
        active_team = self.request.user.userprofile.active_team
        return queryset.filter(created_by=self.request.user,converted_to_client=False,team=active_team)

# @login_required
# def leads_list(request):
#     leads = Lead.objects.filter(created_by=request.user,converted_to_client=False)
#     return render(request,'lead/lead_list.html',{
#         'leads':leads,
#     })

class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))

# @login_required
# def leads_detail(request,pk):
#     lead= get_object_or_404(Lead,created_by=request.user,pk=pk)
#     # lead = Lead.objects.filter(created_by=request.user).get(pk=pk)
#
#     return render(request,'lead/lead_detail.html',{
#         'lead': lead
#     })

class LeadDeleteView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')
    success_message = 'Lead Deleted Successfully!'

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)

# @login_required
# def leads_delete(request,pk):
#     lead= get_object_or_404(Lead,created_by=request.user,pk=pk)
#     lead.delete()
#     messages.success(request,"Lead deleted successfully.")
#
#     return redirect('leads:list')

class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.get_active_team()
        self.object.save()
        add_message(self.request, INFO, f"Lead '{self.object.name}' created successfully!")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.get_active_team()
        context['team'] = team
        context['title'] = 'Add lead'

        return context



# @login_required
# def add_lead(request):
#     team = Team.objects.filter(created_by=request.user)[0]
#     if request.method == 'POST':
#         form = AddLeadForm(request.POST)
#
#         if form.is_valid():
#             team = Team.objects.filter(created_by=request.user)[0]
#             lead = form.save(commit=False)
#             lead.created_by = request.user
#             lead.team = team
#             lead.save()
#             messages.success(request, "Lead created successfully.")
#             return redirect('leads:list')
#     else:
#         form = AddLeadForm()
#     return render(request,'lead/add_lead.html',{
#             'form': form,
#             'team': team
#     })

class LeadUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')
    success_message = 'Lead Edited Successfully'

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit lead'

        return context
# @login_required
# def leads_edit(request,pk):
#     lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
#     if request.method == 'POST':
#         form = AddLeadForm(request.POST,instance=lead)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Changes saved successfully")
#             return redirect('leads:list')
#     else:
#         form = AddLeadForm(instance=lead)
#     return render(request,'lead/leads_edit.html',{
#             'form': form
#     })
class ConvertToClientView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        team = self.request.user.userprofile.active_team
        lead = get_object_or_404(Lead, team=team, pk=pk)
        team = self.request.user.userprofile.get_active_team()

        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team,
        )

        lead.converted_to_client = True
        lead.save()
        comments = lead.comments.all()
        for comment in comments:
            ClientComment.objects.create(
                client = client,
                content = comment.content,
                team = team,
                created_by = comment.created_by,
            )
        # messages.success(request, "Lead converted to client successfully")
        add_message(self.request, INFO, f"Lead '{lead.name}' converted to client successfully!")
        return redirect('leads:list')


# @login_required
# def convert_to_client(request,pk):
#     lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
#     team = Team.objects.filter(created_by=request.user)[0]
#     client = Client.objects.create(
#         name = lead.name,
#         email = lead.email,
#         description = lead.description,
#         created_by = request.user,
#         team=team,
#     )
#     lead.converted_to_client = True
#     lead.save()
#     messages.success(request,"Lead converted successfully")
#     return redirect('leads:list')

class AddCommentView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.get_active_team()
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)
