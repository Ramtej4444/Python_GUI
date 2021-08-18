from tkinter import *
root = Tk()


def create_users(listp):
    file = open("C:\\Users\\Ramtej\\PycharmProjects\\assign2_1\\social_network.txt")
    flag = 0
    for line in file:
        if line.find("#groups") != -1:
            flag = 0

        if flag == 1:
            prs = Person()
            prs.id = extract_parent(line)
            listp.append(prs)

        if line.find('#users') != -1:
            flag = 1


def create_c_list(listp):
    file = open("C:\\Users\\Ramtej\\PycharmProjects\\assign2_1\\social_network.txt")
    flag = 0
    for line in file:
        if line.find("#groups") != -1:
            flag = 0
        if flag == 1:
            parent_id = extract_parent(line)
            contact_list = extract_contacts(line)
            for c in contact_list:
                add_contacts(c, search(parent_id, listp), listp)

        if line.find("#users") != -1:
            flag = 1


def create_groups(list_g, list_m):
    file = open("C:\\Users\\Ramtej\\PycharmProjects\\assign2_1\\social_network.txt")
    flag = 0
    for line in file:
        if flag == 1:
            g = Group()
            g.id = extract_parent(line)
            list_members = extract_contacts(line)
            for c in list_members:
                add_member(c, g, list_m)
            list_g.append(g)

        if line.find("#groups") != -1:
            flag = 1
    file.close()


def add_mem_groups(list_m, list_g):
    for i in range(len(list_m)):
        temp = mem_sfor_group(list_m[i], list_g)
        for j in range(len(temp)):
            list_m[i].grouplist.append(search(temp[j], list_g))


def extract_parent(temp):
    par = temp.split(' ', 1)[0]
    par = par.replace(':', '')
    return par


def extract_contacts(temp):
    details = temp.split()
    details.pop(0)
    for i in range(len(details)):
        details[i] = details[i].replace(',', '')
    return details


def add_member(m_id, group, list_m):
    group.memberslist.append(search(m_id, list_m))


def mem_sfor_group(user, list_g):
    temp = []
    for y in range(len(list_g)):
        for z in range(len(list_g[y].memberslist)):
            if user.id == list_g[y].memberslist[z].id:
                temp.append(list_g[y].id)

    return temp


def add_contacts(c_id, parent, listp):
    parent.contactlist.append(search(c_id, listp))


def search(temp, listp):
    for x in range(len(listp)):
        if listp[x].id == temp:
            return listp[x]


class Person:
    def __init__(self):
        self.id = ""
        self.contactlist = []
        self.grouplist = []
        self.rec_posts = []

    def receive(self, temp):
        self.rec_posts.append(temp)
        start = self.id + "++"
        end = self.id + "--"
        with open("C:\\Users\\Ramtej\\PycharmProjects\\assign2_1\\message.txt", 'a') as file:
            file.write(start+"\n")
            file.write(temp)
            file.write(end+"\n")

    def update_contacts(self, frame):
        frame.contact_list.delete(0, END)
        for i in range(len(self.contactlist)):
            frame.contact_list.insert(i, self.contactlist[i].id)

    def update_groups(self, frame):
        frame.group_list.delete(0, END)
        for i in range(len(self.grouplist)):
            frame.group_list.insert(i, self.grouplist[i].id)

    def update_message(self, frame):
        frame.message_list.delete(0, END)
        for i in range(len(self.rec_posts)):
            frame.message_list.insert(i, self.rec_posts[i])


class Group:
    def __init__(self):
        self.id = ""
        self.memberslist = []
        self.posts = []


class CurrentUser(Frame):
    def __init__(self, master=None, list_u=None,
                 c_frame=None, g_frame=None, mes_frame=None):
        Frame.__init__(self, master)
        self.master = master
        self.list_u = list_u
        self.c_frame = c_frame
        self.g_frame = g_frame
        self.mes_frame = mes_frame
        self.config(bg="SlateBlue3")
        self.grid(row=0, column=2)
        self.users_ = Label(self.master, text="Current User", height=1,
                           bg="SteelBlue4", fg="ivory2")
        self.users_.grid(row=0,column=3)
        self.users_.config(font=25)
        self.welcome = Label(self.master, text="R_NETWORKS_R", bg="springgreen2",
                             width=40, height=2)
        self.welcome.grid(row=0,column=0, columnspan=2)
        self.welcome.config(font=120)
        self.users = Label(self, text="Choose an User ", height=3,
                           bg="SlateBlue1", fg="ivory2")
        self.users.grid(row=0)
        self.users_list = Listbox(self, fg="grey15", bg="azure2")
        self.users_list.grid(row=1, column=0, padx=4, pady=5, sticky=S + N + E + W)
        for i in range(len(self.list_u)):
            self.users_list.insert(END, self.list_u[i].id)
        self.button = Button(self, text="Select", width=15, height=5,
                              command=self.select_user, bg="RoyalBlue2", fg="ivory2")
        self.button.grid(row=1, column=1, sticky=N)
        self.exitbutton = Button(self, text="EXIT", command=exit, width=15, height=5,
                                 bg="RoyalBlue2", fg="ivory2")
        self.exitbutton.grid(row=1, column=1, sticky=S)
        self.st = ""
        for i in range(len(list_u)):
            self.retrieve(list_u[i].id)

    def select_user(self):
        self.c_frame.update_c(search(self.users_list.get(ANCHOR), self.list_u))
        self.g_frame.update_g(search(self.users_list.get(ANCHOR), self.list_u))
        self.mes_frame.update_m(search(self.users_list.get(ANCHOR), self.list_u))
        self.st = self.users_list.get(ANCHOR)
        self.users_.config(text=self.st)

    def current_user(self):
        return self.st

    def retrieve(self,cur):
        file = open("C:\\Users\\Ramtej\\PycharmProjects\\assign2_1\\message.txt")
        start = cur + "++"
        end = cur + "--"
        flag = 0
        for line in file:
            if line.find(end) != -1:
                flag = 0

            if flag == 1:
                search(cur, self.list_u).rec_posts.append(line)

            if line.find(start) != -1:
                flag = 1


class Contacts(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(row=1, column=0)
        self.config(bg="MistyRose2")
        self.contact_label = Label(self, text="Contact List", bg="RoyalBlue1", fg="ivory2",
                                   width=30, height=3)
        self.contact_label.grid(row=0, column=0, padx=4, pady=5)
        self.contact_list = Listbox(self, fg="grey15", bg="azure2")
        self.contact_list.grid(row=1, column=0,
                               padx=4, pady=5, sticky=S + N + E + W)

    def update_c(self, p=None):
        p.update_contacts(self)


class Groups(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(row=1, column=1)
        self.config(bg="MistyRose2")
        self.group_label = Label(self, text="Groups List", bg="RoyalBlue1", fg="ivory2",
                                 width=30, height=3)
        self.group_label.grid(row=0, column=0, padx=4, pady=5)
        self.group_list = Listbox(self, fg="grey15", bg="azure2")
        self.group_list.grid(row=1, column=0,
                             padx=4, pady=5, sticky=S + N + E + W)

    def update_g(self, p=None):
        p.update_groups(self)


class Messages(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(row=1, column=3)
        self.config(bg="MistyRose2")
        self.message = Label(self, text="Messages Received", bg="RoyalBlue1", fg="ivory2",
                             width=30, height=3)
        self.message.grid(row=0, column=0, padx=4, pady=5)
        self.message_list = Listbox(self, fg="grey15", bg="azure2")
        self.message_list.grid(row=1, column=0,
                               padx=4, pady=5, sticky=S + N + E + W)

    def update_m(self, p=None):
        p.update_message(self)


class PostMessages(Frame):
    def __init__(self, master=None, c_frame=None, g_frame=None,
                 in_frame=None, list_u=None, list_g=None):
        Frame.__init__(self, master)
        self.master = master
        self.g_frame = g_frame
        self.c_frame = c_frame
        self.list_u = list_u
        self.list_g = list_g
        self.in_frame = in_frame
        self.grid(row=1, column=2)
        self.config(bg="MistyRose2")
        self.message = Label(self, text="Enter The Message Below", bg="RoyalBlue1", fg="ivory2",
                             width=30, height=3)
        self.message.grid(row=0, column=0, padx=4, pady=5)
        self.message_ = Text(self, width=30, height=8, fg="grey15", bg="azure2")
        self.message_.grid(row=1, column=0,
                           padx=4, pady=5)
        self.frame_buttons = Frame(self, bg="thistle1")
        self.frame_buttons.grid(row=3, sticky="news")
        self.sendbutton = Button(self.frame_buttons, text="SEND", command=self.send_msg, width=16)
        self.sendbutton.grid(row=0, column=0, sticky="news")
        self.sendbutton2 = Button(self.frame_buttons, text="SEND TO GROUP", command=self.send_msg_grp,
                                  width=17)
        self.sendbutton2.grid(row=0, column=3, sticky=E)

    def send_msg(self):
        msg = self.message_.get(1.0, END)
        ki = self.in_frame.current_user()
        msg = ki + " : " + msg
        search(self.c_frame.contact_list.get(ANCHOR), self.list_u).receive(msg)

    def send_msg_grp(self):
        msg = self.message_.get(1.0, END)
        ki = self.in_frame.current_user()
        gr_name = self.g_frame.group_list.get(ANCHOR)
        msg = gr_name + "::" + " " + ki + " : " + msg
        g_range = len(search(self.g_frame.group_list.get(ANCHOR), self.list_g).memberslist)
        for i in range(g_range):
            if search(self.g_frame.group_list.get(ANCHOR), self.list_g).memberslist[i].id != ki:
                search(self.g_frame.group_list.get(ANCHOR), self.list_g).memberslist[i].receive(msg)
            

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.config(bg="thistle3")
        self.grid(row=0, column=0)
        self.cont = Contacts(self.master)
        self.group = Groups(self.master)
        self.mess = Messages(self.master)
        self.cframe = CurrentUser(self.master, user_list, self.cont,
                                  self.group, self.mess)
        self.post = PostMessages(self.master, self.cont, self.group,
                                 self.cframe, user_list, group_list)


group_list = []
user_list = []
create_users(user_list)
create_c_list(user_list)
create_groups(group_list, user_list)
add_mem_groups(user_list, group_list)

adv = Window(root)
adv.mainloop()
