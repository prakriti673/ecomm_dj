from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation

# Create your views here.

# if you click on the contact seller button, you will be sent here  
# opening up a new conversation between you(User) and the seller()
@login_required
def new_conversation(request, item_pk):
    # getting the item you selected
    item=get_object_or_404(Item, pk=item_pk)

    # if the user clicks on contacting seller of the product which he has himself listed, we redirect him to the dashboard
    if item.created_by == request.user:
        return redirect('dashboard:index')
     
    # filtering out all the conversations in which the user (active user) is a part of with the item in context being the item clicked on
    conversations= Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # we check if the active user has previously also contacted the seller of this item, and if so, a conversation already exists
    if conversations:
        return redirect('conversation:detail',pk=conversations.first().id)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail',pk=item_pk)
        
    else:
        form = ConversationMessageForm()

    return render(request,'conversation/new_conversation.html',{
        'form':form
    })

@login_required
def inbox(request):
    conversations= Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations' : conversations
    })

@login_required
def detail(request,pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form= ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form=ConversationMessageForm()


    return render(request,'conversation/detail.html',{
        'conversation' : conversation,
        'form' : form,
    })

