from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Students,Lecture
from .models import Post
from .forms import PostForm,TeachPost
from app1.models import Section_class,Students
from itertools import chain
# Create your views here.
def Post_view(request):      #for students temp
	if request.user.is_student:
		if not Students.objects.filter(email=request.user).count():
			return redirect("/app1/profile")
	post_query=[]
	section_list=[]
	section_id=[]
	drake=[]
	if request.user.is_teacher:
		obj=Lecture.objects.filter(user__id=request.user.id)
		print(obj)
		query1=[]
		for sec in obj:
			query1.append(int(sec.section_class.id))
		query1=list(dict.fromkeys(query1))
		print(query1)
		section_list=query1
		print(section_list)
		for sec in section_list:
			drake=Post.objects.filter(section__id=str(sec)).order_by('date_posted')
			drake=drake.reverse()
			post_query=list(chain(post_query,drake))
		

		if request.POST:
			form=TeachPost(request.POST or None)
			if form.is_valid():
				instance=form.save(commit=False)
				instance.user=request.user
				print(instance.user)
				instance.save()
				return redirect("/posts")
		else:
			form=TeachPost()
			form.fields['section'].queryset = Section_class.objects.filter(lecture__user=request.user).distinct()

		context={'posts':post_query,'form':form}
		return render(request,"myposts.html",context)

	elif request.user.is_student:
		query1=Students.objects.get(email=request.user.email)
		print(query1.section)
		section_list=query1.section
		section_id=Students.objects.get(email=request.user.email)
		post_query=Post.objects.filter(section=query1.section).order_by('date_posted')
		print("########################")
		print(Post.objects.all())
		print(post_query)
		post_query=post_query.reverse()
		

		if request.POST:
			print(request.POST)
			title=request.POST.get('Title')
			description=request.POST.get('description')
			instance=Post(section=section_id.section,user=request.user,title=title,description=description)
			instance.save()
			print(instance)
			return redirect("bloggy:posts")
	

		context={'posts':post_query}
		return render(request,"posts.html",context)


def myPost_view(request):      #for students temp
	post_query=[]
	section_list=[]
	section_id=[]
	drake=[]
	if request.user.is_teacher:
		obj=Lecture.objects.filter(user__id=request.user.id)
		print(obj)
		query1=[]
		for sec in obj:
			query1.append(int(sec.section_class.id))
		query1=list(dict.fromkeys(query1))
		print(query1)
		section_list=query1
		print(section_list)
		for sec in section_list:
			drake=Post.objects.filter(section__id=str(sec),user=request.user).order_by('date_posted')
			post_query=list(chain(post_query,drake))
		

		if request.POST:
			form=TeachPost(request.POST or None)
			if form.is_valid():
				instance=form.save(commit=False)
				instance.user=request.user
				print(instance.user)
				instance.save()
				return redirect("/posts/myPosts")
		else:
			form=TeachPost()
			form.fields['section'].queryset = Section_class.objects.filter(lecture__user=request.user).distinct()

		context={'posts':post_query,'form':form}
		return render(request,"myposts.html",context)

	elif request.user.is_student:
		query1=Students.objects.get(email=request.user.email)
		print(query1.section)
		section_list=query1.section
		section_id=Students.objects.get(email=request.user.email)
		post_query=Post.objects.filter(section=query1.section,user=request.user).order_by('date_posted')
		post_query=post_query.reverse()
		

		if request.POST:
			print(request.POST)
			title=request.POST.get('Title')
			description=request.POST.get('description')
			instance=Post(section=section_id.section,user=request.user,title=title,description=description)
			instance.save()
			print(instance)
			return redirect("bloggy:posts")
	

		context={'posts':post_query}
		return render(request,"myposts.html",context)


def editpost(request,my_id):
	obj=get_object_or_404(Post,id=my_id)
	print(my_id)

	if request.user.is_student:
		form=PostForm(request.POST or None,instance=obj)
	else:
		form=TeachPost(request.POST or None,instance=obj)
	if form.is_valid():
		form.save()
		return redirect("/posts/myPosts")
	context={
	"form":form,"title":obj
	}
	return render(request,"forms.html",context)



def post_delete(request,my_id):         #delete post
	obj=get_object_or_404(Post,id=my_id)
	print(my_id)
	if request.POST:
		obj.delete()
		return redirect("/posts/myPosts")
	context={
	"object":obj
	}
	return render(request,"deletepost.html",context)




def teacher_post_view(request,my_id=None):  #TAB VIEW
	post_query=[]
	section_list=[]
	section_id=[]
	drake=[]
	aloo=[]		
	sect="Select Class"
	obj=Lecture.objects.filter(user__id=request.user.id)
	print(obj)
	query1=[]
	for sec in obj:
		query1.append(sec.section_class)
	query1=list(dict.fromkeys(query1))
	print(query1)
	section_list=query1
	print(section_list)
	for sec in section_list:
		aloo.append(sec)
	flag=1
	if my_id:
		flag=0
		sect=Section_class.objects.get(id=my_id)
		post_query=Post.objects.filter(section__id=my_id)
		post_query=post_query[::-1]
		print("uno")
		for post in post_query:
			print(post)

	if request.POST:
		if not my_id==None:
			sec=Section_class.objects.get(id=my_id)
			form=PostForm(request.POST or None)
		else:
			form=TeachPost(request.POST or None)
		if form.is_valid():
			instance=form.save(commit=False)
			if my_id:
				instance.section=Section_class.objects.get(id=my_id)
			instance.user=request.user
			print(instance.user)
			instance.save()
			if not my_id==None:
				ret="/posts/myTeachPosts/"+str(my_id)
				return redirect(ret)
			return redirect("/posts/myTeachPosts")
		print("didnt validate")
	else:
		if my_id==None:
			form=TeachPost()
			form.fields['section'].queryset = Section_class.objects.filter(lecture__user=request.user).distinct()
		else:
			sec=Section_class.objects.get(id=my_id)
			form=PostForm()
			
				

	context={'posts':post_query,'form':form,'aloo':aloo,'dont':my_id,'flag':flag,'sec':sect}
	return render(request,"teach2.html",context)

		


