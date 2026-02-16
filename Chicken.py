# -*- coding: utf-8 -*-
# coding: utf-8

import telebot
import glob, os ,sys
import time
from telebot import types
import shutil
from datetime import date
import time
import random
import threading
import math
import sqlite3
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import logging
import traceback
import re
import json;
from telebot.types import InputMediaPhoto
lang = "ru"
file = open("name_bot.txt","r")
name_bot = file.read()
file.close()

file = open("channel","r")
channel = file.read()
file.close()
#channel=str(104932971);

file = open("channel_drivers","r")
channel_drivers = file.read()
file.close()
#channel_drivers=str(104932971);

MAX_ORDERS=40;
time_for_delivery = 1
key_hard = False
f = open("pass","r");
PASS = f.read().replace("\n","");
f.close()
DEBUG = False;
max_debug = False
DAYS = ["Dushanba","Понедельник","Chorshanba","Вторник","Seshanba","Среда","Payshanba","Четверг","Juma","Пятница","Shanba","Суббота","Yakshanba","Воскресенье"];
DAYSRU = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"];
DAYS2=["22","23","24","25","26","27","28","29","30"];
Tables=["day22","day23","day24","day25","day26","day27","day28","day29","day30","day1","day2","day3","day4","day5","day6","day7"];
DAYS=DAYS+DAYS2;
Districts=["Чиланзар","Сергели","Яккасарай","Мирабад","Яшнабад","Мирзо-Улугбек","Юнус-Абад","Шайхантахур","Алмазар","Куйлюк","Бектемир","Учтепа","Неизвестно"];


t=time.time()
#logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'mylog.log')

file = open("token","r")
token = file.read().replace("\n","");
file.close();
#token="7373030023:AAEpSJfV3-yCU2GRZbcf7Q7_wXk-7d8tGkI";
try:
    f = open("/home/tom/itsHome","r");
    f.close();
    #bot = telebot.TeleBot("1667410978:AAG6n31W6BI38fxVLzEexbzkFoy_wHmpgPo") #TEST
    bot = telebot.TeleBot(token)
except:
    bot = telebot.TeleBot(token)

def check_posts():
    try:
        try:
            file = open("post_info/get_start_post","r")
            get_start_post = file.read()
            file.close()
        except:
            get_start_post = "0"
        if get_start_post != "1":
            pass
        else:
            file = open("post_info/post_text","r")
            post_text = file.read()
            file.close()

            file = open("post_info/link","r")
            link = file.read()
            file.close()

            file = open("post_info/admin","r")
            admin = file.read()
            file.close()

            file = open("post_info/cat","r")
            cat = file.read()
            file.close()

            users = os.listdir("post_info/users")
            for i in range(len(users)):
                try:
                    os.remove("post_info/users/"+users[i])
                except Exception as e:
                    logger(e)
                time.sleep(0.2)
                user = users[i].replace(".sqlite","")
                try:
                    if post_text != "not":
                        bot.send_message(user,str(post_text))
                    if link == "1":
                        try:
                            photo = open("post/post.jpg",'rb')
                            bot.send_photo(user, photo,caption=post_text);
                            photo.close()
                        except:
                            bot.send_message(user,str(post_text))
                    else:
                        photo = open("post/post.jpg",'rb')
                        bot.send_photo(user, photo);
                        photo.close()
                    file = open("post_info/active","r")
                    active = int(file.read())
                    file.close()
                    file = open("post_info/active","w")
                    file.write(str(active+1))
                    file.close()
                    #bot.send_message(admin,"ok: "+str(users[i]))
                except:
                    file = open("post_info/not_active","r")
                    not_active = int(file.read())
                    file.close()
                    file = open("post_info/not_active","w")
                    file.write(str(not_active+1))
                    file.close()
                    #bot.send_message(admin,"bad: "+str(users[i]))

                if len(users) == int(i)+1:
                    file = open("post_info/not_active","r")
                    not_active = int(file.read())
                    file.close()
                    file = open("post_info/active","r")
                    active = int(file.read())
                    file.close()
                    try:
                        time_off = str(datetime.now())
                        file = open("post_info/time_on","r")
                        time_on = file.read()
                        file.close()
                        bot.send_message(admin,"\nВремя начала: "+str(time_on)+"\nВремя окончания: "+str(time_off))
                    except:
                        pass
                    bot.send_message(admin,"Активных: "+str(active)+"\nНеактивных: "+str(not_active))

            try:
                os.remove("post/post.jpg")
            except:
                pass
            bot.send_message(admin,"Рассылка прошла успешно")
            file = open("post_info/get_start_post","w")
            file.write("0")
            file.close()
            state(message,"link","0")
    except Exception as e:
        logger(message,e)

post_check = threading.Thread(target=check_posts, args=())
post_check.start()

def start_all(message):
    try:
        users=os.listdir("users");
        for u in users:
            os.remove("users/"+u);
    except:
        pass;

@bot.message_handler(commands=['stat_all'])
def all_Stat(message):
    give_stat(message,"all");
@bot.message_handler(commands=['stat_day'])
def day_Stat(message):
    give_stat(message,"day");
@bot.message_handler(commands=['stat_month'])
def month_Stat(message):
    give_stat(message,"month");

def give_stat(message,time_var):
    try:
        data = statistic_read(time_var);
        pic1 = open("graph.png","rb");
        bot.send_photo(message.from_user.id, pic1);
        pic1.close();

        try:
            pic2 = open("graph_price.png","rb")
            bot.send_photo(message.from_user.id, pic2,caption=data);
            pic2.close()
        except:
            pic2 = open("graph_price.png","rb")
            bot.send_photo(message.from_user.id, pic2);
            pic2.close()
            bot.send_message(message.chat.id,data)
        os.remove("graph.png")
        os.remove("graph_price.png")
    except:
        bot.send_message(message.chat.id,"Статистика пуста")


@bot.message_handler(commands=['clear_stat'])
def clear_stat(message):
    chat_id = message.chat.id
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM day_stat''')
    conn.commit()
    conn.close()

@bot.message_handler(commands=['ru'])
def ru_lang(message):
    state(message,"lang","ru")
    start(message)

@bot.message_handler(commands=['uz'])
def uz_lang(message):
    state(message,"lang","uz")
    start(message)

@bot.message_handler(commands=['start'])
def restart(message):
    try:
        try:

            photo = open("img/label.jpg",'rb')
            #bot.send_photo(message.from_user.id, photo);
            photo.close()
        except:
            pass
        #try:
        #    shutil.rmtree("users/"+str(message.from_user.id))
        #except:
        #    pass
        try:
            db_new_user(message)
            state(message,"step","start")
        except:
            os.remove("users/"+str(message.chat.id)+".sqlite")
            db_new_user(message)
        state(message,"lang","ru")
        bot_register_next_step_handler(message,"start")
        start(message)
    except Exception as e:
        logger(message,e)

@bot.message_handler(content_types=["text"])
def marsh(message):
    try:
        current_datetime = datetime.now()
        stoped = os.listdir()
        if "ban" in stoped:
            print("stopped")
        else:
            try:
                files = os.listdir("/home/bogdan/SBCS2.0/ban_list")
            except:
                files = []
            if str(message.chat.id) in files:
                bot.send_message(message.chat.id, "БАН!")
            else:
                hour = 11# int(current_datetime.hour)
                if int(hour)>= 20 or int(hour) < 8:
                    bot.send_message(message.chat.id, "Мы работаем с 8:00 до 20:00")
                else:
                    file=open('prof','r');
                    v=file.read();
                    file.close();
                    if v=='❌' or message.chat.id == 104932971 or message.chat.id ==1841650:
                        marsh1(message)
                    else:
                        bot.send_message(message.chat.id, "🛠В боте проходят технические работы, извините за неудобства⚙️")
    except Exception as e:
        logger(message,e)

def marsh1(message):
    try:
        try:
            step = state_read(message,"step")
        except:
            db_new_user(message)
            state(message,"step","start")
            step = state_read(message,"step")
        try:
            lang = state_read(message,"lang")
        except:
            state(message,"lang","ru")
        if message.text == "raiseErr":
            1+"1"
        if message.text == "step":
            bot.send_message(message.chat.id,state_read(message,"step"))
        if message.text == "📥 Savat":
            bot_register_next_step_handler(message,"basket_choise")
        if step == "start":
            start(message)
        elif step == "start_second":
            start_second(message)
        elif step == "check_choise":
            check_choise(message)
        elif step == "how_many_podcat":
            how_many_podcat(message)
        elif step == "basket_choise":
            basket_choise(message)
        elif step == "get_contact":
            get_contact(message)
        elif step == "save_contact":
            save_contact(message)
        elif step == "save_loc":
            save_loc(message)
        elif step == "send":
            send(message)
        elif step == "check_admin":
            check_admin(message)
        elif step == "start1":
            start1(message)
        elif step == "new_review":
            new_review(message)
        elif step == "check_pass":
            check_pass(message)
        elif step == "get_comment":
            get_comment(message)
        elif step == "create_cat":
            create_cat(message)
        elif step == "create_prod":
            create_prod(message)
        elif step == "change_info":
            change_info(message)
        elif step == "change_done":
            change_done(message)
        elif step == "on_cat":
            on_cat(message)
        elif step == "on_podcat":
            on_podcat(message)
        elif step == "get_time":
            get_time(message)
        elif step == "cat_change_name":
            cat_change_name(message)
        elif step == "prod_change_name":
            prod_change_name(message)
        elif step == "change_pass":
            change_pass(message)
        elif step == "driver_on":
            driver_on(message)
        elif step == "driver_off":
            driver_off(message)
        elif step == "new_or_old":
            new_or_old(message)
        elif step == "new_orders":
            new_orders(message)
        elif step == "old_orders":
            old_orders(message)
        elif step == "change_orders":
            change_orders(message)
        elif step == "get_pay_form":
            get_pay_form(message)
        elif step == "give_for_number":
            give_for_number(message)
        elif step == "give_for_number2":
            give_for_number2(message)
        elif step == "give_for_number3":
            give_for_number3(message)
        elif step == "change_information":
            change_information(message)
        elif step == "get_day_del":
            get_day_del(message)
        elif step == "getTxtAdres":
            getTxtAdres(message)
        elif step == "check_new_post1":
            check_new_post1(message)
        elif step == "check_new_post":
            check_new_post(message)
        elif step == "getTxtAdres":
            getTxtAdres(message)
        elif step == "change_days":
            change_days(message)
        elif step == "getContactName":
            getContactName(message)
        elif step == "delete_order":
            delete_order(message)
        elif step == "checkDistrict":
            checkDistrict(message)


    except Exception as e:
        logger(message,e)

def start(message):
    try:
        state(message,"admin_active","0")
        try:
            lang = state_read(message,"lang")
        except:
            lang = "ru"
        current_datetime = datetime.now()
        if lang == "ru":
            bot.send_message(message.chat.id, "Привет! Добро пожаловать в официальный Бот <strong>Курочки Неженки</strong>\nДля смены языка нажмите /ru или /uz",reply_markup=keyboard_menu(message),parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Salom! Rasmiy <strong>Курочки Неженки</strong> Bot-ga xush kelibsiz \nTilni o'zgartirish uchun /ru yoki /uz",reply_markup=keyboard_menu(message),parse_mode='HTML')
        bot_register_next_step_handler(message, "start1");
    except Exception as e:
        logger(message,e)

def start1(message):
    try:
        lang = state_read(message,"lang")
        if message.text == "people":
            files = len(os.listdir("users"))
            bot.send_message(message.chat.id, files)
        elif message.text == "test":
            stringParser(message,testDel)
        elif "ℹ️" in message.text:
            checkSendLog(message);
            file = open("Info.txt","r")
            info = file.read();
            file.close();
            bot.send_message(message.chat.id, info);

        elif message.text == "Qo`llab-quvvatlash xizmati📳" or message.text == "Служба поддержки📳":
            if lang == "ru":
                bot.send_message(message.chat.id, "Служба поддержки📳",reply_markup=keyboard_site2(message))
            else:
                bot.send_message(message.chat.id, "Qo`llab-quvvatlash xizmati📳",reply_markup=keyboard_site2(message))
        elif message.text == "Продукция" or message.text == "Mahsulotlar":
            try:
                data = db_img_cat_read(message," ");
                bot.send_photo(message.chat.id,data);
            except Exception as e:
                logger(message,e)
            if lang == "uz":
                bot.send_message(message.chat.id, "Menyu",reply_markup=keyboard(message))
            else:
                bot.send_message(message.chat.id, "Меню",reply_markup=keyboard(message))
            bot_register_next_step_handler(message, "start_second");
        elif message.text == "admin" or message.text == "Admin":
            state(message,"lang","ru")
            if message.chat.id == 104932971 or message.chat.id == 217718167:
                admin(message);
            else:
                bot.send_message(message.chat.id, "Пароль",reply_markup=keyboard_back(message));
                bot_register_next_step_handler(message, "check_pass");
        elif message.text == "📥 Savat" or message.text == "📥 Корзина":
            basket(message)
        elif message.text == "☎️Kontaktlar" or message.text == "☎️Контакты":
            if lang == "ru":
                bot.send_message(message.chat.id, "По вопросам заказов обращаться: \n+998937884677",reply_markup=keyboard_group(message))
            else:
                bot.send_message(message.chat.id, "Buyurtmalar bo'yicha murojaat qiling:\n+998937884677",reply_markup=keyboard_group(message))
        elif message.text == "Fikr bildiring✍️" or message.text == "Оставить отзыв✍️":
            if lang == "uz":
                bot.send_message(message.chat.id, "Sharhingizni yozing, fikr-mulohaza biz uchun juda muhimdir)",reply_markup = keyboard_back(message))
            else:
                bot.send_message(message.chat.id, "Напишите свой отзыв, нам важна обратная связь",reply_markup = keyboard_back(message))
            bot_register_next_step_handler(message,"new_review")
        elif message.text == "🇺🇿🔄🇷🇺":
            try:
                lang = state_read(message,"lang")
            except:
                state(message,"lang","ru")
                lang = state_read(message,"lang")
            if lang == "ru":
                state(message,"lang","ru")
            else:
                state(message,"lang","ru")
            start(message)
        else:
            start(message)
    except Exception as e:
        logger(message,e)

def new_review(message):
    try:
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            start(message)
        else:
            #bot.send_message(channel,"Отзыв\n✍️✍️✍️✍️✍️✍️\n"+str(message.text)+"\n✍️✍️✍️✍️✍️✍️")
            if lang == "uz":
                bot.send_message(channel,"Fikr-mulohaza\n"+str(message.text))
                bot.send_message(message.chat.id, "Спасибо за отзыв😁")
            else:
                bot.send_message(channel,"Отзыв\n"+str(message.text))
                bot.send_message(message.chat.id, "Fikr-mulohazangiz uchun rahmat, biz siz bilan birga rivojlanmoqdamiz😁")
            start(message)

    except Exception as e:
        logger(message,e)

def start_second(message):
    try:
        lang = state_read(message,"lang")
        path = path_read(message)
        message_text = message.text.replace("","").replace("","")
        product = is_product(message,message_text)
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            if len(path_read(message))==0:
                admin_active = state_read(message,"admin_active")
                if admin_active == "0":
                    start(message)
                else:
                    admin(message)
            else:
                path_rem(message)
                if lang == "uz":
                    bot.send_message(message.chat.id, "Menyu",reply_markup=keyboard(message))
                else:
                    bot.send_message(message.chat.id, "Меню",reply_markup=keyboard(message))

        elif  message.text == "📥 Savat" or message.text == "📥 Корзина" or "Оформить" in message.text:
            bot_register_next_step_handler(message, "basket_choise");
            basket(message)
        elif message.text == "🚖 Tekshirib ko'rmoq" or message.text == "🚖 Оформить заказ":
            bot_register_next_step_handler(message, "basket_choise");
            basket(message)
        elif message.text == "admin" or message.text == "Admin":
            state(message,"lang","ru")
            if message.chat.id == 104932971 or message.chat.id == 217718167:
                admin(message);
            else:
                bot.send_message(message.chat.id, "Пароль",reply_markup=keyboard_back(message));
                bot_register_next_step_handler(message, "check_pass");
        elif message.text == "Создать продукт":
            bot.send_message(message.chat.id, "Введите имя категории",reply_markup=keyboard_back(message))
            bot_register_next_step_handler(message, "create_prod");
        elif message.text == "Создать категорию":
            bot.send_message(message.chat.id, "Введите имя категории",reply_markup=keyboard_back(message))
            bot_register_next_step_handler(message, "create_cat");
        elif message.text == "Удалить категорию":
            del_some(message,"cat")
        elif message.text == "Удалить фото категории":
            del_cat_prod_photo(message,"cat")
        elif message.text == "Изменить имя категории":
            bot.send_message(message.chat.id, "Введите имя категории",reply_markup=keyboard_back(message))
            state(message,"change_var_cat","ru")
            bot_register_next_step_handler(message, "cat_change_name");
        elif message.text == "Изменить узб имя категории":
            bot.send_message(message.chat.id, "Введите узб имя категории",reply_markup=keyboard_back(message))
            state(message,"change_var_cat","uz")
            bot_register_next_step_handler(message, "cat_change_name");


        elif product:
            print("this is product")
            admin_active = state_read(message,"admin_active")
            state(message,"podcat",message_text)
            if admin_active == "0":
                try:
                    conn = sqlite3.connect('db.sqlite')
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT img_have FROM product WHERE name = '"+str(message_text)+"'")
                        img_have = cursor.fetchall()[0][0]
                    except:
                        cursor.execute("SELECT img_have FROM product WHERE name_uz = '"+str(message_text)+"'")
                        img_have = cursor.fetchall()[0][0]
                    conn.close()
                    if img_have == "1":
                        data = db_img_read(message,message_text);
                        bot.send_photo(message.chat.id,data);
                except Exception as e:
                    logger(message,e)
                check_choise(message);
            else:
                make_changes(message)
        else:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT img_have FROM category WHERE name = '"+str(message_text)+"'")
                img_have = cursor.fetchall()[0][0]
            except:
                cursor.execute("SELECT img_have FROM category WHERE name_uz = '"+str(message_text)+"'")
                img_have = cursor.fetchall()[0][0]
            conn.close()

            if img_have == "1":
                data = db_img_cat_read(message,message_text);
                bot.send_photo(message.chat.id,data);
            new_path(message,message.text)
            if lang == "uz":
                bot.send_message(message.chat.id, "Menyu",reply_markup=keyboard(message))
            else:
                bot.send_message(message.chat.id, "Меню",reply_markup=keyboard(message))
    except Exception as e:
        logger(message,e)

def cat_change_name(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            l = state_read(message,'change_var_cat')
            path = path_read(message)
            cat = path[len(path)-1]
            cat_id = get_cat_id(message,cat)
            name = message.text.replace("'","`").replace('"','``')
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            if l == "ru":
                cursor.execute("UPDATE category SET name = '"+str(name)+"' WHERE id = '"+cat_id+"'")
            else:
                cursor.execute("UPDATE category SET name_uz = '"+str(name)+"' WHERE id = '"+cat_id+"'")
            results = cursor.fetchall();
            conn.commit();
            conn.close();
            bot.send_message(message.chat.id, "Изменено");
            admin(message);
    except Exception as e:
        logger(message,e)

def prod_change_name(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            l = state_read(message,'change_var_prod')
            path = path_read(message)
            cat = path[len(path)-1]
            cat_id = get_cat_id(message,cat)
            conn = sqlite3.connect('db.sqlite')
            name = message.text.replace("'","`").replace('"','``')
            cursor = conn.cursor()
            if l == "ru":
                cursor.execute("UPDATE product SET name = '"+str(name)+"' WHERE cat_id = '"+cat_id+"'")
            else:
                cursor.execute("UPDATE product SET name_uz = '"+str(name)+"' WHERE cat_id = '"+cat_id+"'")
            results = cursor.fetchall();
            conn.commit();
            conn.close();
            bot.send_message(message.chat.id, "Изменено");
            admin(message);
    except Exception as e:
        logger(message,e)

def is_product(message,message_text):
    try:
        lang = state_read(message,"lang")
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        if lang == "ru":
            cursor.execute("SELECT name FROM product");
        else:
            cursor.execute("SELECT name_uz FROM product");
        results = cursor.fetchall()
        files = []
        for i in range(len(results)):
            files.append(results[i][0])
        conn.close()
        return message_text in files
    except Exception as e:
        logger(message,e)

def check_pass(message):
    try:
        if message.text == PASS:
            bot_register_next_step_handler(message, "check_admin");
            admin(message)
        else:
            start(message)
    except Exception as e:
        logger(message,e)

def admin(message):
    try:
        state(message,"admin_active","1")
        path_rem_all(message)
        bot.send_message(message.chat.id, "панель администратора",reply_markup=keyboard_admin(message))
        bot_register_next_step_handler(message, "check_admin");
    except Exception as e:
        logger(message,e)

def check_admin(message):
    try:
        if message.text == "⬅️ Назад":
            start(message)
        elif 'Профилактика' in message.text:
            if '❌' in message.text:
                d='✅';
            else:
                d='❌';
            file=open('prof','w')
            file.write(d);
            file.close();
            bot.send_message(message.chat.id, "Изменено",reply_markup=keyboard_admin(message))
        elif message.text == "Отправить заказы":
            bot.send_message(message.chat.id,"Выберете день",reply_markup=keyboard_inline_days(message));
        elif message.text == "Удалить заказ":
            bot.send_message(message.chat.id,"Введите номер заказа для удаления",reply_markup=keyboard_back(message));
            bot_register_next_step_handler(message,"delete_order");
        elif message.text == "Изменить дни":
            bot.send_message(message.chat.id,"Выберете день",reply_markup=keyboard_change_days(message));
            bot_register_next_step_handler(message,"change_days")
        elif message.text == "Изменить адрес":
            bot.send_message(message.chat.id,"Выберете день",reply_markup=keyboard_location_admin(message));
            bot_register_next_step_handler(message,"change_information")
        elif message.text == "Изменить инфо":
            bot.send_message(message.chat.id,"Введите текст инфо",reply_markup=keyboard_back(message));
            bot_register_next_step_handler(message,"change_information")
        elif message.text == "Сделать рассылку":
            new_post1(message);
        elif message.text == "Перебросить заказы":
            if message.chat.id == 104932971 or message.chat.id == 217718167:
                bot.send_message(message.chat.id,"Новые заказы или остатки",reply_markup=keyboard_new_or_old(message));
                bot_register_next_step_handler(message,"new_or_old")
        elif message.text == "Перебросить по номеру":
            if message.chat.id == 104932971 or message.chat.id == 217718167:
                bot.send_message(message.chat.id,"Напишите номер",reply_markup=keyboard_back(message));
                bot_register_next_step_handler(message,"give_for_number")
        elif message.text == "Вернуть всех в начало":
            start_all(message)
        elif message.text == "Внести изменения":
            create(message)
        elif message.text == "Включить категорию":
            on_cat_podcat(message,"cat")
        elif message.text == "Включить подкатегорию":
            on_cat_podcat(message,"podcat")
        elif message.text == "Включить водителя":
            bot.send_message(message.chat.id,"Выберете водителя",reply_markup=keyboard_on_driver(message));
            bot_register_next_step_handler(message,"driver_on")
        elif message.text == "Выключить водителя":
            bot.send_message(message.chat.id,"Выберете водителя",reply_markup=keyboard_off_driver(message));
            bot_register_next_step_handler(message,"driver_off")
        elif message.text == "Сменить пароль":
            bot.send_message(message.chat.id,"Введите новый пароль",reply_markup=keyboard_back(message));
            bot_register_next_step_handler(message,"change_pass")
    except Exception as e:
        logger(message,e)

def delete_order(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            num = message.text
            try:
                int(num)+1;
                base("DELETE FROM orders WHERE num = '{0}'".format(num));
                admin(message);
                bot.send_message(message.chat.id,"Удален заказ "+num);
            except:
                bot.send_message(message.chat.id,"Неккоректный номер заказа");
    except Exception as e:
        logger(message,e);

def change_days(message):
    try:
        if "⬅️" in message.text:
            admin(message);
        else:
            ms = message.text
            if "❌" in ms:
                pos = True;
            elif "✅" in ms:
                pos = False;
            if "Понедельник" in ms:
                day = "day1";
            elif "Вторник" in ms:
                day = "day2";
            elif "Среда" in ms:
                day = "day3";
            elif "Четверг" in ms:
                day = "day4";
            elif "Пятница" in ms:
                day = "day5";
            elif "Суббота" in ms:
                day = "day6";
            elif "Воскресенье" in ms:
                day = "day7";
            #
            ms=ms.replace("✅","").replace("❌","")
            try:
                int(ms)+1;
                n=True;
            except:
                n=False
            print(DAYS);
            print(ms)
            if n and ms in DAYS:
                day="day"+ms;
            #

            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            if pos:
                insert = "✅"
            else:
                insert = "❌"
            cursor.execute("UPDATE days SET '"+day+"' = '"+str(insert)+"'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id,"Выберете день",reply_markup=keyboard_change_days(message));
    except Exception as e:
        logger(message,e);


def send_day_orders(message,base):
    base=int(base.replace("day",""));
    if base>0 and base <=7:
        day=DAYSRU[base-1];
    else:
        day=str(base);
    ords=db("SELECT json FROM orders WHERE status = '1' AND day = '{0}'".format(day));
    nakTxt="";
    nak={"sum":"0"};
    allSum=0;
    allCount=0
    for o in ords:
        js=json.loads(o);
        if js!=None:
            try:
                print(len(js))
            except:
                print(type(js),"<<<<<<This");
                print(js,"<<<<<<");
            for i in range(len(js)):
                if js[i]['name'] in nak:
                    nak[js[i]['name']]=str(int(nak[js[i]['name']])+int(js[i]['how_many']));
                else:
                    nak[js[i]['name']]=js[i]['how_many'];
                prodSum=int(js[i]['how_many'])*int(js[i]['price']);
                nak['sum']=str(int(nak['sum'])+prodSum);
                allCount=allCount+int(js[i]['how_many'])
    bot.send_message(message.chat.id, "Накладная готовиться, подождите немного . . .");
    i=1;
    for n in nak:
        if n!='sum':
            nakTxt=nakTxt+'\n№'+str(i)+' '+n+' x '+nak[n];
            i+=1;
    d=datetime.now();
    date="{0}.{1}.{2}".format(str(d.day),str(d.month),str(d.year));

    nakTxt=nakTxt+'\n\nВсего единиц товара: '+str(allCount);
    nakTxt=nakTxt+'\nОбщая сумма: '+nak['sum']+' сум';
    nakTxt=nakTxt+'\nДата: '+date;

    nakTxt = re.sub(r"🦃|🐔|🐂|🐄|🥩|🍖|😋|🐇|🐦‍🔥|🦆|🪿", "", nakTxt)
    nakTxt='Накладная:\n'+nakTxt;
    bot.send_message(message.chat.id, nakTxt);
    bot.send_message(channel_drivers, nakTxt);
    last_indexForSend=[];
    for district in Districts:
        time.sleep(0.5);
        last_indexForSend=db("SELECT num FROM orders WHERE district='{0}' AND status = '1' AND day = '{1}'".format(district,day,));
        for last_index in last_indexForSend:
            time.sleep(0.5)
            data=db("SELECT basket FROM orders WHERE num = '{0}'".format(last_index,))[0];
            lon=db("SELECT lon FROM orders WHERE num = '{0}'".format(last_index,))[0];
            lat=db("SELECT lat FROM orders WHERE num = '{0}'".format(last_index,))[0];
            try:
                bot.send_message(channel_drivers, data,reply_markup=keyboard_send_loc(message,last_index));
                db("UPDATE orders SET status = '2' WHERE num = '{0}'".format(last_index,));
                if lat != "0":
                    bot.send_location(channel_drivers,float(lat),float(lon));
            except Exception as e:
                logger(message,e);
                s=checkSendLog(message);
                bot.send_message(message.chat.id, "Были отправлены не все заказы, попробуйте снова через {0} секунд.\n Но накладная уже готова".format(s));
                break;
                break;
        print(district+': Отправлен');
    bot.send_message(message.chat.id, "Все заказы отправлены");


def send_day_orders2(message,base):
    try:
        conn = sqlite3.connect('days.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM '"+base+"'")
        data = cort_to_list(cursor.fetchall());
        cursor.execute("SELECT lon FROM '"+base+"'")
        lon = cort_to_list(cursor.fetchall());
        cursor.execute("SELECT lat FROM '"+base+"'")
        lat = cort_to_list(cursor.fetchall());
        cursor.execute("SELECT last_index FROM '"+base+"'")
        last_index = cort_to_list(cursor.fetchall());
        oneDel = ""
        bot.send_message(message.chat.id, "Накладная готовиться, подождите немного . . .");
        for i in range(len(data)):
            oneDel+="\n"+data[i];
        nak = stringParser(message,oneDel);
        try:
            d=datetime.now();
            date="{0}.{1}.{2}".format(str(d.day),str(d.month),str(d.year));
        except:
            date="errorDate"
        bot.send_message(message.chat.id, "Накладная:\n"+nak+"\n"+date);

        for district in Districts:
            time.sleep(0.4)
            for i in range(len(data)):
                dist=get_district(data[i]);
                if district==dist:
                    try:
                        time.sleep(0.4)
                        bot.send_message(channel_drivers, data[i],reply_markup=keyboard_send_loc(message,last_index[i]));
                        if lat != "0":
                            bot.send_location(channel_drivers,float(lat[i]),float(lon[i]))
                        save_in_history(data[i],lon[i],lat[i],last_index[i]);
                        cursor.execute("DELETE FROM '"+base+"' WHERE data = '"+data[i]+"'")
                        conn.commit();
                    except Exception as e:
                        logger(message,e);
                        s=checkSendLog(message);
                        bot.send_message(message.chat.id, "Были отправлены не все заказы, попробуйте снова через {0} секунд.\n Но накладная уже готова".format(s));
                        break;

        
        conn.commit();
        conn.close();
    except Exception as e:
        logger(message,e);

def checkSendLog(message):
    file = open("log/mylog.txt","r")
    data=file.read();
    file.close()
    if 'Too Many Requests' in data:
        data=data[::-1].replace('\n','');
        s='';
        for i in range(len(data)):
            if data[i]==' ':
                break;
            else:
                s+=data[i];
        s=s[::-1];
        print(int(s),'<4');
        return s;
    else:
        return 'ok';

def save_in_history(data,lon,lat,last_index):
    conn = sqlite3.connect('orders.sqlite');
    cursor = conn.cursor();
    cursor.execute("INSERT INTO orders VALUES ((?),(?),(?),(?),(?))",("0",data,lon,lat,last_index));
    conn.commit();
    conn.close();

def change_information(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            file = open("Info.txt","w");
            file.write(message.text);
            file.close();
            bot.send_message(message.chat.id,"Инфо изменено на "+message.text);
            admin(message);
    except Exception as e:
        logger(message,e);

def change_pass(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            file = open("pass","w");
            file.write(message.text);
            file.close();
            bot.send_message(message.chat.id,"Пароль изменен на "+message.text);
            admin(message);
    except Exception as e:
        logger(message,e);

def on_cat_podcat(message,var):
    try:
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        if var == "cat":
            cursor.execute("SELECT name FROM category WHERE work = '0'");
        else:
            cursor.execute("SELECT name FROM product WHERE work = '0'");
        results = cursor.fetchall();
        conn.close();
        files = [];
        for i in range(len(results)):
            files.append(results[i][0]);
        bot.send_message(message.chat.id, "Выберете для включения",reply_markup=keyboard_on_cat_podcat(message,files));
        if var =="cat":
            bot_register_next_step_handler(message,"on_cat")
        else:
            bot_register_next_step_handler(message,"on_podcat")
    except Exception as e:
        logger(message,e)
def on_cat(message):
    try:
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        cursor.execute("UPDATE category SET work = '1' WHERE name = '"+str(message.text)+"'");
        conn.commit();
        conn.close();
        bot.send_message(message.chat.id, "Включено");
        admin(message)
    except Exception as ec:
        logger(message,e)
def on_podcat(message):
    try:
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        cursor.execute("UPDATE product SET work = '1' WHERE name = '"+str(message.text)+"'");
        conn.commit();
        conn.close();
        bot.send_message(message.chat.id, "Включено");
        admin(message)
    except Exception as e:
        logger(message,e)
def del_some(message,var):
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        path = path_read(message)
        cat = path[len(path)-1]
        if var =="cat":
            cat_id = get_cat_id_for_cat(message,cat)
            cursor.execute("UPDATE category SET work = '0' WHERE cat_id = '"+str(cat_id)+"' AND name = '"+cat+"'")
        else:
            cat_id = get_cat_id(message,cat)
            cat = state_read(message,"podcat")
            cursor.execute("UPDATE product SET work = '0' WHERE cat_id = '"+str(cat_id)+"' AND name = '"+cat+"'")
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Удалено")
        admin(message)
    except Exception as e:
        logger(message,e)
def del_cat_prod_photo(message,var):
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        path = path_read(message)
        cat = path[len(path)-1]
        cat_id = get_cat_id_for_cat(message,cat)
        print(cat)
        if var == "cat":
            cursor.execute("UPDATE category SET img = NULL WHERE cat_id = '"+str(cat_id)+"' AND name = '"+cat+"'")
            cursor.execute("UPDATE category SET img_have = '0' WHERE cat_id = '"+str(cat_id)+"' AND name = '"+cat+"'")
        else:
            cat_id = get_cat_id(message,cat)
            cat = state_read(message,"podcat")
            cursor.execute("UPDATE product SET img = NULL WHERE cat_id = '"+str(cat_id)+"' AND name = '"+cat+"'")
            cursor.execute("UPDATE product SET img_have = '0' WHERE cat_id = '"+str(cat_id)+"' AND name = '"+cat+"'")
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Удалено")
        admin(message)
    except Exception as e:
        logger(message,e)
def create(message):
    try:
        bot.send_message(message.chat.id, "Выберете действие",reply_markup=keyboard(message))
        bot_register_next_step_handler(message,"start_second")
    except Exception as e:
        logger(message,e)
def create_cat(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            name = message.text.replace("'","`").replace('"','``')
            cursor.execute("SELECT id FROM category WHERE name = '"+str(name)+"'")
            results = cursor.fetchall()
            cursor.execute("SELECT id FROM category")
            cats = cursor.fetchall()
            path = path_read(message)
            try:
                cat = path[len(path)-1]
                cat_id = get_cat_id(message,cat)
            except:
                cat_id = "0";
            index = str(len(cats)+1)
            if len(results) == 0:
                cursor.execute("INSERT INTO category VALUES ((?),(?),(?),(?),(?),(?), NULL )",(cat_id,index,name,name,'1','0'))
            else:
                cursor.execute("UPDATE category SET work = '1' WHERE name = '"+str(name)+"'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Категория создана",reply_markup=keyboard(message))
            path_rem_all(message)
            admin(message);
    except Exception as e:
        logger(message,e)
def create_prod(message):
    try:
        if "Назад" in message.text:
            admin(message);
        else:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            name = message.text.replace("'","`").replace('"','``')
            cursor.execute("SELECT id FROM product")
            cats = cursor.fetchall()
            path = path_read(message)
            try:
                cat = path[len(path)-1]
                cat_id = get_cat_id(message,cat)
            except:
                cat_id="0";
            cursor.execute("SELECT id FROM product WHERE name = '"+str(name)+"'")
            results = cursor.fetchall()
            cursor.execute("SELECT id FROM product WHERE name = '"+str(name)+"' AND cat_id = '"+cat_id+"'")
            results2 = cursor.fetchall()

            index = str(len(cats)+1)
            if len(results2) == 0:
                cursor.execute("INSERT INTO product VALUES ((?),(?),(?),(?),(?),(?),(?),(?),(?),NULL)",(cat_id,index,name,name,'1','0','_','_','0'))
            else:
                cursor.execute("UPDATE product SET work = '1' WHERE name = '"+str(name)+"'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Продукт создан",reply_markup=keyboard(message))
            path_rem_all(message)
            admin(message);
    except Exception as e:
        logger(message,e)
def make_changes(message):
    try:
        bot.send_message(message.chat.id, "Выберете действие",reply_markup=keyboard_changes(message))
        bot_register_next_step_handler(message,"change_info")
    except Exception as e:
        logger(message,e)
def change_info(message):
    try:
        if "Назад" in message.text :
            bot.send_message(message.chat.id, "Выберете действие",reply_markup=keyboard(message));
            bot_register_next_step_handler(message,"start_second");
        else:
            if message.text == "Изменить цену":
                var = "price";
            elif message.text == "Изменить описание":
                var = "rev";
            elif message.text == "Добавить узб описание":
                var = "rev_uz";
            elif message.text == "Добавить узб имя":
                var = "name_uz";
            elif message.text == "Добавить фото":
                var = "img";
            elif message.text == "Удалить фото":
                var = "img_del";
                del_cat_prod_photo(message,"prod");
            elif message.text == "Удалить продукт":
                var = "del";
                del_some(message,"prod");
            elif message.text == "Изменить имя продукта":
                var = "del";
                bot.send_message(message.chat.id, "Введите новое имя продукта",reply_markup=keyboard_back(message))
                state(message,"change_var_prod","ru")
                bot_register_next_step_handler(message, "prod_change_name");
            if var !="del" and var != "img_del":
                state(message,"change_var",var);
                bot.send_message(message.chat.id, "Введите данные (отправьте фото)",reply_markup=keyboard_back(message))
                bot_register_next_step_handler(message,"change_done")
    except Exception as e:
        logger(message,e)
def change_done(message):
    try:
        if "Назад" in message.text:
            bot.send_message(message.chat.id, "Выберете действие",reply_markup=keyboard(message));
            bot_register_next_step_handler(message,"start_second");
        else:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            var = state_read(message,"change_var")
            path = path_read(message)
            message_text = message.text.replace("'","`").replace('"','``')
            try:
                cat = path[len(path)-1]
                cat_id = get_cat_id(message,cat)
            except:
                cat_id="0";
            name = state_read(message,"podcat")
            cursor.execute("UPDATE product SET "+var+" = '"+str(message_text)+"' WHERE name = '"+str(name)+"' AND cat_id = '"+cat_id+"'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Изменения внесены")
            admin(message)
    except Exception as e:
        logger(message,e)
def new_post1(message):
    try:
        bot.send_message(message.chat.id,"Напишите текст поста",reply_markup=keyboard_photo(message))
        bot_register_next_step_handler(message,"check_new_post")
    except Exception as e:
        logger(message,e)
def check_new_post(message):
    try:
        if "Назад" in message.text or "Orqaga" in message.text:
            state(message,"link","0")
            admin(message)
        else:
            if message.text == "Пропустить":
                text = "not"
            else:
                text = str(message.text)
            state(message,"new_post",str(text))
            bot.send_message(message.chat.id,"Отправьте фото",reply_markup=keyboard_back(message))
            bot_register_next_step_handler(message,"check_new_post1")
    except Exception as e:
        logger(message,e)
def check_new_post1(message):
    try:
        if message.text == "Пропустить":
            y = threading.Thread(target=pre_admin, args=(message,))
            y.start()
            x = threading.Thread(target=send_post, args=(message,))
            x.start()

        elif "Назад" in message.text or "Orqaga" in message.text in message.text:
            state(message,"link","0")
            admin(message)
        else:
            pass
    except Exception as e:
        logger(message,e)
def pre_admin(message):
    try:
        bot.send_message(message.chat.id,"Рассылка началась")
        admin(message)
        state(message,"link","0")
    except Exception as e:
        logger(message,e)
def send_post(message):
    try:
        if max_debug == True:
            photo = open("post/post.jpg",'rb')
            user = 104932971
            bot.send_photo(user, photo,reply_markup=keyboard_post(message));
            photo.close()
        else:
            post_text = state_read(message,"new_post")
            link = state_read(message,"link")
            file = open("post_info/post_text","w")
            file.write(str(post_text))
            file.close()
            file = open("post_info/link","w")
            file.write(str(link))
            file.close()
            file = open("post_info/admin","w")
            file.write(str(message.chat.id))
            file.close()

            file = open("post_info/active","w")
            file.write("0")
            file.close()
            file = open("post_info/not_active","w")
            file.write("0")
            file.close()
            try:
                time_on = str(datetime.now())
                file = open("post_info/time_on","w")
                file.write(time_on)
                file.close()
            except:
                pass
            users = os.listdir("users")
            for i in range(len(users)):
                file = open("post_info/users/"+users[i].replace(".sqlite",""),"w")
                file.write("")
                file.close()
            file = open("post_info/get_start_post","w")
            file.write("1")
            file.close()


            users = os.listdir("post_info/users")
            for i in range(len(users)):
                try:
                    os.remove("post_info/users/"+users[i])
                except:
                    pass
                time.sleep(0.2)
                user = users[i].replace(".sqlite","")
                try:
                    if post_text != "not":
                        try:
                            photo = open("post/post.jpg",'rb')
                            bot.send_photo(user, photo,caption=post_text);
                            photo.close()
                        except:
                            bot.send_message(user,str(post_text))
                    else:
                        photo = open("post/post.jpg",'rb')
                        bot.send_photo(user, photo);
                        photo.close()
                    file = open("post_info/active","r")
                    active = int(file.read())
                    file.close()
                    file = open("post_info/active","w")
                    file.write(str(active+1))
                    file.close()
                    #bot.send_message(message.chat.id,"ok: "+str(users[i]))

                except Exception as e:
                    #logger(message,e)
                    file = open("post_info/not_active","r")
                    not_active = int(file.read())
                    file.close()
                    file = open("post_info/not_active","w")
                    file.write(str(not_active+1))
                    file.close()
                    #bot.send_message(message.chat.id,"bad: "+str(users[i]))

                if len(users) == int(i)+1:
                    file = open("post_info/not_active","r")
                    not_active = int(file.read())
                    file.close()
                    file = open("post_info/active","r")
                    active = int(file.read())
                    file.close()
                    try:
                        time_off = str(datetime.now())
                        file = open("post_info/time_on","r")
                        time_on = file.read()
                        file.close()
                        bot.send_message(message.chat.id,"\nВремя начала: "+str(time_on)+"\nВремя окончания: "+str(time_off))
                    except Exception as e:
                        logger(e)
                    bot.send_message(message.chat.id,"Активных: "+str(active)+"\nНеактивных: "+str(not_active))

            try:
                os.remove("post/post.jpg")
            except:
                pass
            bot.send_message(admin,"Рассылка прошла успешно")
            file = open("post_info/get_start_post","w")
            file.write("0")
            file.close()
            state(message,"link","0")
    except Exception as e:
        logger(message,e)
#+++++++++++++++++фото
def new_photo(message):
    try:
        bot.send_message(message.chat.id, "Выберете раздел",reply_markup=keyboard0(message))
        bot_register_next_step_handler(message, "new_photo0");
    except Exception as e:
        logger(message,e)
def new_photo0(message):
    try:
        if "Назад" in message.text or "Orqaga" in message.text:
            admin(message)
        else:
            state(message,"part",message.text)
            bot.send_message(message.chat.id, "Название категории",reply_markup=keyboard_cat(message))
            bot_register_next_step_handler(message, "check_new_photo");
    except Exception as e:
        logger(message,e)
def check_new_photo(message):
    try:
        if "Назад" in message.text or "Orqaga" in message.text:
            bot.send_message(message.chat.id, "Выберете раздел",reply_markup=keyboard0(message))
            bot_register_next_step_handler(message, "new_photo0");
        else:
            state(message,"cat",str(message.text))
            new_photo1(message)
    except Exception as e:
        logger(message,e)
def new_photo1(message):
    try:
        bot.send_message(message.chat.id, "Название подкатегории",reply_markup=keyboard_podcat(message))
        bot_register_next_step_handler(message, "check_new_photo1");
    except Exception as e:
        logger(message,e)
def check_new_photo1(message):
    try:
        if message.text == "⬅️ Orqaga" or "Назад" in message.text:
            new_photo(message)
        else:
            state(message,"podcat",str(message.text))
            new_photo2(message)
    except Exception as e:
        logger(message,e)
def new_photo2(message):
    try:
        bot.send_message(message.chat.id, "Отправьте фото",reply_markup=keyboard_back(message))
        bot_register_next_step_handler(message, "check_new_photo2");
    except Exception as e:
        logger(message,e)
@bot.message_handler(content_types=['photo'])
def check_new_photo2(message):
    try:
        step = state_read(message,"step")
        admin_active = state_read(message,"admin_active")
        if step  == "check_new_post1":
            try:
                file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = "post/post.jpg"

                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                y = threading.Thread(target=pre_admin, args=(message,))
                y.start()
                x = threading.Thread(target=send_post, args=(message,))
                x.start()
            except:
                pass
        elif step == "change_done":
            file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            data = downloaded_file

            path = path_read(message)
            try:
                cat = path[len(path)-1]
                cat_id = get_cat_id(message,cat)
            except:
                cat_id = "0";
            name = state_read(message,"podcat")

            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM product WHERE name = '"+str(name)+"' AND cat_id = '"+str(cat_id)+"'")
            results = cursor.fetchall()[0][0]
            cursor.execute("UPDATE product SET img_have = '1' WHERE id = (?)",(results,))
            conn.close()

            db_img_write(data,str(results))
            bot.send_message(message.chat.id, "Фото добавлено")
            admin(message)


        elif step == "start_second" and admin_active == "1":

            path = path_read(message)
            try:
                cat = path[len(path)-1]
            except:
                cat = " "
            file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            data = downloaded_file

            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("UPDATE category SET img_have = '1' WHERE name = (?)",(cat,))
            binary = sqlite3.Binary(data)
            cursor.execute("UPDATE category  SET img = (?)  WHERE name = (?)",(binary, cat))
            conn.commit()
            conn.rollback()
            conn.close()
            bot.send_message(message.chat.id, "Фото добавлено")
            admin(message)
        else:
            pass
           #bot.send_message(message.chat.id, "Да, а еще теперь ты заблокирован, и у меня твой айди. Выбрасывай мобильник пока я тебя сука не нашел, ты мне столько проблем сделал")

    except Exception as e:
        logger(message,e)
def check_choise(message):
   # try:
        lang = state_read(message,"lang")
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            if lang == "uz":
                bot.send_message(message.chat.id, "Menyu",reply_markup=keyboard(message))
            else:
                bot.send_message(message.chat.id, "Меню",reply_markup=keyboard(message))
            bot_register_next_step_handler(message, "start_second");
        elif message.text == "⏬Ro'yxat" or message.text == "⏬Список":
            list_pro(message)
        elif message.text == "📥 Savat" or message.text == "📥 Корзина" or message.text == "🚖 Оформить заказ" or message.text == "🚖 Tekshirib ko'rmoq":
            basket(message)
        else:
            message_text = message.text.replace("","").replace("","")
            state(message,"podcat",message_text)
            path = path_read(message)
            #cat = path[len(path)-1]
            podcat  = message_text
            try:
                data = product_price(message,str(podcat))
                rev = product_rev(message,str(podcat))
            except:
                data = product_price_uz(message,str(podcat))
                rev = product_rev_uz(message,str(podcat))
            if rev == "_":
                rev = " "
            if lang == "uz":
                bot.send_message(message.chat.id, "Miqdorini tanlang yoki kiriting:",reply_markup=keyboard_num(message))
            else:
                bot.send_message(message.chat.id, "Выберите или введите количество:",reply_markup=keyboard_num(message))
            bot_register_next_step_handler(message, "how_many_podcat");
            if lang == "ru":
                bot.send_message(message.chat.id,rev+"\n\nЦена: "+data+"сум")
                bot_register_next_step_handler(message, "how_many_podcat");
            else:
                bot.send_message(message.chat.id,rev+"\n\nNarxi: "+data+"so`m")
                bot_register_next_step_handler(message, "how_many_podcat");
            bot_register_next_step_handler(message, "how_many_podcat");

    #except Exception as e:
    #    logger(message,e)
def list_pro(message):
    try:
        lang = state_read(message,"lang")
        if lang == "ru":
            cat = state_read(message,"cat")
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM category WHERE name = '"+str(cat)+"'")
            results = cursor.fetchall()
            conn.close()
            str_files = results[0][0]
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM product WHERE work = '1' AND cat_id = '"+str(str_files)+"'")
            results = cursor.fetchall()
            cursor.execute("SELECT name FROM product WHERE work = '0' AND cat_id = '"+str(str_files)+"'")
            results2 = cursor.fetchall()
            conn.close()
            data = ""
            lang = state_read(message,"lang")
            for i in range(len(results)):
                podcat = results[i][0]
                price = product_price(message,podcat)
                if lang == "ru":
                    data+="\n"+podcat+" - "+price
                else:
                    data+="\n"+podcat+" - "+price
            for i in range(len(results2)):
                podcat = results2[i][0]
                if lang == "ru":
                    data+="\n"+podcat+" - Нет в наличии"
                else:
                    data+="\n"+podcat+" - Нет в наличии"
            bot.send_message(message.chat.id,data)
        else:
            cat = state_read(message,"cat")
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM category WHERE name_uz = '"+str(cat)+"'")
            results = cursor.fetchall()
            conn.close()
            str_files = results[0][0]
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT name_uz FROM product WHERE work = '1' AND cat_id = '"+str(str_files)+"'")
            results = cursor.fetchall()
            cursor.execute("SELECT name_uz FROM product WHERE work = '0' AND cat_id = '"+str(str_files)+"'")
            results2 = cursor.fetchall()
            conn.close()
            data = ""
            lang = state_read(message,"lang")
            for i in range(len(results)):
                podcat = results[i][0]
                price = product_price_uz(message,podcat)
                if lang == "ru":
                    data+="\n"+podcat+" - "+price
                else:
                    data+="\n"+podcat+" - "+price
            for i in range(len(results2)):
                podcat = results2[i][0]
                if lang == "ru":
                    data+="\n"+podcat+" - Нет в наличии"
                else:
                    data+="\n"+podcat+" - Нет в наличии"
            bot.send_message(message.chat.id,data)


    except Exception as e:
        logger(message,e)
def how_many_podcat(message):
    try:
        lang = state_read(message,"lang")
        path = path_read(message)
        try:
            cat = path[len(path)-1]
        except:
            cat = ""
        podcat = state_read(message,"podcat")
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            if lang == "uz":
                bot.send_message(message.chat.id, "Menyu",reply_markup=keyboard(message))
            else:
                bot.send_message(message.chat.id, "Меню",reply_markup=keyboard(message))
            bot_register_next_step_handler(message, "start_second");
        elif message.text == "📥 Savat" or message.text == "📥 Корзина" or "Оформить" in message.text:
            basket(message)
        elif message.text == "⏩":
            if lang == "uz":
                bot.send_message(message.chat.id, "Miqdorini tanlang yoki kiriting:",reply_markup=keyboard_num1(message))
            else:
                bot.send_message(message.chat.id, "Выберите или введите количество:",reply_markup=keyboard_num1(message))
        elif message.text == "⏮":
            if lang == "uz":
                bot.send_message(message.chat.id, "Miqdorini tanlang yoki kiriting:",reply_markup=keyboard_num1(message))
            else:
                bot.send_message(message.chat.id, "Выберите или введите количество:",reply_markup=keyboard_num1(message))
        else:
            message_text = message.text.replace("кг","").replace("шт","")
            try:
                ms=message_text;
                if message_text=="0.5":
                    message_text="1";
                int(message_text)+1
                if "Печень" in podcat and int(message_text)<3:
                    bot.send_message(message.chat.id, "Бота так не проведешь😉")
                else:
                    if "Фарш" in podcat and ms=="0.5" and "говяжий" not in podcat:
                        price="35000"
                    else:
                        try:
                            price = product_price(message,str(podcat))
                        except:
                            price = product_price_uz(message,str(podcat))
                    basket_add(message,cat+" | "+podcat,str(price),str(message_text))
                    state(message,podcat,"")
                    if lang == "uz":
                        bot.send_message(message.chat.id, "Sizning buyurtmangiz menyuda joylashgan savatga qo'shildi",reply_markup=keyboard(message))
                    else:
                        bot.send_message(message.chat.id, "Ваш заказ был добавлен в корзину, расположенную в меню",reply_markup=keyboard(message))
                    path = path_read(message);
                    bot_register_next_step_handler(message, "start_second");

            except Exception as e:
                logger(message,e)
                if lang == "uz":
                    bot.send_message(message.chat.id, "Kiritish xatosi, qayta urinib ko‘ring",reply_markup=keyboard_num(message))
                else:
                    bot.send_message(message.chat.id, "Ошибка ввода, пожалуйста, попробуйте еще раз",reply_markup=keyboard_num(message))
    except Exception as e:
        logger(message,e)
def get_comment(message):
    try:
        lang = state_read(message,"lang")
        podcat = state_read(message,"podcat")
        state(message,podcat,message.text)
        if lang == "uz":
            bot.send_message(message.chat.id, "Sizning buyurtmangiz menyuda joylashgan savatga qo'shildi",reply_markup=keyboard_pro(message))
           # bot.send_message(message.chat.id, "Menyuni ko'rish yoki mahsulotni tanlash uchun '⏬Ro yxat' ni bosing",reply_markup=keyboard_pro(message))
        else:
            bot.send_message(message.chat.id, "Ваш заказ был добавлен в корзину, расположенную в меню",reply_markup=keyboard_pro(message))
           # bot.send_message(message.chat.id, "Нажмите « ⏬ Список » для ознакомления с меню или выберите товар",reply_markup=keyboard_pro(message))
        bot_register_next_step_handler(message, "check_choise");
    except Exception as e:
        logger(message,e)
def basket(message):
    try:
        lang = state_read(message,"lang")
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            start(message)
        else:
            files = basket_show(message)
            if len(files)==0:
                if lang =="uz":
                    bot.send_message(message.chat.id, "Savatingiz bo'sh, buyurtma beradigan narsani tanlang",reply_markup=keyboard(message))
                else:
                    bot.send_message(message.chat.id, "Корзина пуста, сначала выберете что то из меню",reply_markup=keyboard(message))
                start(message)

            else:
                if lang == "uz":
                    bot.send_message(message.chat.id, "❌ Ism - bitta narsani o'chirish\n🔄 Bo'sh - savatni to'liq bo'shating")
                else:
                    bot.send_message(message.chat.id, "«❌ Наименование » - удалить одну позицию\n«🔄 Очистить » - полная очистка корзины")

                if lang == "uz":
                    state(message,"buf","Savat:\n")
                else:
                    state(message,"buf","Корзина:\n")
                basket = basket_show(message)
                saldo_end = 0
                buf=state_read(message,'buf');
                for i in range(len(basket)):
                    basket_ = basket[i].replace(".txt","")
                    buf=buf+str("\n№"+str(i+1)+" "+basket_);
                    price = basket_price(message,str(basket[i]))
                    how_many = basket_how_many(message,str(basket[i]))
                    saldo = int(how_many)*int(price)
                    saldo_end = int(saldo_end)+int(saldo)
                    buf=buf+str("\n"+str(how_many)+" x "+str(price)+" = "+str(saldo)+"\n");
                    try:
                        com = state_read(message,basket_)
                        buf=buf+"Доп. контакт: "+com;
                    except:
                        pass
                print(buf);
                if lang == "uz":
                    buf=buf+"\nJami: "+str(saldo_end)+" сум";
                else:
                    buf=buf+"\nИтого: "+str(saldo_end)+" сум";
                state(message,"end_price",str(saldo_end))
                state(message,'buf',buf)
                bot.send_message(message.chat.id, buf,reply_markup=keyboard_basket(message))
                if lang == "ru":
                    bot.send_message(message.chat.id, (10*"👇")+"\n👉Цена приблизительная👈\n"+(10*"👆"),reply_markup=keyboard_basket(message))
                else:
                    bot.send_message(message.chat.id, (10*"👇")+"\n👉Цена приблизительная👈\n"+(10*"👆"),reply_markup=keyboard_basket(message))
                bot_register_next_step_handler(message, "basket_choise");
    except Exception as e:
        logger(message,e)
        bot.send_message(message.chat.id, "Ваша корзина была исправлена")
        basket_del_all(message)
        start(message)
        bot.send_document(104932971, open("log/mylog.txt",'rb'))
def basket_choise(message):
    try:
        lang = state_read(message,"lang")
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            if lang == "uz":
                bot.send_message(message.chat.id, "Menyu",reply_markup=keyboard(message))
            else:
                bot.send_message(message.chat.id, "Меню",reply_markup=keyboard(message))
            bot_register_next_step_handler(message, "start_second");
        elif message.text == "📥 Savat" or message.text == "📥 Корзина":
            basket(message)
        elif message.text == "🚖 Tekshirib ko'rmoq" or message.text == "🚖 Оформить заказ":
            get_contact(message);
        elif message.text == "Aniq" or message.text == "Очистить":
            basket_del_all(message)
            if lang=="uz":
                bot.send_message(message.chat.id,"Savat bo'sh",reply_markup=keyboard_basket(message))
            else:
                bot.send_message(message.chat.id,"Корзина пуста",reply_markup=keyboard_basket(message))
            basket(message)
        else:
            ans = message.text.replace("❌","")
            ans = ans.replace("","").replace("","")
            basket_del(message,ans)
            if lang == "uz":
                bot.send_message(message.chat.id,"Olib tashlandi",reply_markup=keyboard_basket(message))
            else:
                bot.send_message(message.chat.id,"Удалено",reply_markup=keyboard_basket(message))
            basket(message)
    except Exception as e:
        logger(message,e)
def get_contact(message):
    try:
        lang = state_read(message,"lang")
        files = basket_show(message)
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            basket(message)
        elif len(files) == 0:
            if lang == "uz":
                bot.send_message(message.chat.id,"Savatingiz bo'sh. Iltimos, avval biron narsa buyurtma qiling")
            else:
                bot.send_message(message.chat.id,"Ваша корзина пуста. Пожалуйста, закажите что-нибудь сначала")
        else:
            if lang == "uz":
                bot.send_message(message.chat.id,"Iltimos, kontaktni yuboring yoki qo'lda yozing",reply_markup=keyboard_contact(message))
            else:
                bot.send_message(message.chat.id,"Пожалуйста, отправьте контакт или напишите вручную",reply_markup=keyboard_contact(message))
            bot_register_next_step_handler(message,"save_contact")
    except Exception as e:
        logger(message,e)
@bot.message_handler(content_types=["contact"])
def save_contact(message):
    lang = L(message.chat.id);
    try:
        if message.content_type !="contact":
            message_text = message.text.replace(" ","")
        if message.content_type !="contact" and len(message_text)<9:
            if lang == "ru":
                bot.send_message(message.chat.id,"Пожалуйста введите номер с кодом, Цифрами")
            else:
                bot.send_message(message.chat.id,"Iltimos to'liq raqamlarni Raqamlarda kiriting")
            get_contact(message)
        else:
            try:
                if message.content_type =="contact":
                    num_phone = message.contact.phone_number
                elif int(message_text)*1:
                    num_phone = message_text
                if len(num_phone)==9:
                    num_phone="+998"+num_phone;
                elif len(num_phone)==12:
                    num_phone="+"+num_phone;
                state(message,"contact",str(num_phone))
                get_loc(message)
            except Exception as e:
                print(e)
                if lang == "ru":
                    bot.send_message(message.chat.id,"Неккоректный ввод")
                else:
                    bot.send_message(message.chat.id,"Noto'g'ri kiritish")
                get_contact(message)
    except Exception as e:
        logger(message,e)
def get_loc(message):
    try:
        lang = state_read(message,"lang")
        if lang == "uz":
            bot.send_message(message.chat.id,"Iltimos, manzilini yuboring yoki manzilini yozing (Tuman, ko'cha, uy raqami, manzil belgisi).",reply_markup=keyboard_location(message))
        else:
            bot.send_message(message.chat.id,"Пожалуйста, отправьте локацию",reply_markup=keyboard_location(message))# или напишите адрес (Район, улица, номер дома, ориентир).",reply_markup=keyboard_location(message))
        bot_register_next_step_handler(message,"save_loc")
    except Exception as e:
        logger(message,e)
@bot.message_handler(content_types=["location"])
def save_loc(message):
    try:
        if message.content_type == "location":
            step = state_read(message,"step");
            if step == "save_loc":
                longitude = message.location.longitude
                latitude = message.location.latitude
                geo_url = "https://geocode-maps.yandex.ru/1.x?%20format=json&lang=ru_RU&kind=house&geocode="+str(longitude)+","+str(latitude)+"&apikey=dcc7de33-5acb-4746-9558-a2bfbccc8391"
                coords = str(longitude)+","+str(latitude)
                data = str(get_address_from_coords(message,coords))
                #bot.send_message(message.chat.id,data)

                state(message,"longitude",message.location.longitude)
                state(message,"latitude",message.location.latitude)
                state(message,"adres",data);
                adr=get_district(data);
                if "Неизвестно" in adr or 'не установлен':
                    getDistrict(message);
                else:
                    sender(message)
            elif step == "change_information":
                longitude = message.location.longitude
                latitude = message.location.latitude
                file = open("adres/longitude.txt","w")
                file.write(str(longitude))
                file.close()
                file = open("adres/latitude.txt","w")
                file.write(str(latitude))
                file.close()
                bot.send_message(message.chat.id,"Адрес изменен!")
                admin(message);
        else:
            if message.text == "⬅️ Orqaga" or "Назад" in message.text:
                start(message)
            else:
                pass
                adres = message.text;
                if "🏃‍♂️" in adres:
                    file = open("adres/longitude.txt","r")
                    lon = file.read()
                    file.close()
                    file = open("adres/latitude.txt","r")
                    lat = file.read()
                    file.close()
                    bot.send_message(message.chat.id,"Вот наш адрес:")
                    bot.send_location(message.chat.id,float(lat),float(lon));
                    state(message,"adres",adres)
                    state(message,"longitude","0")
                    state(message,"latitude", "0")
                    sender(message)
                else:
                    pass
                
    except Exception as e:
        logger(message,e)
def getDistrict(message):
    l=L(message.chat.id);
    if l=="ru":
        bot.send_message(message.chat.id,"Выберете район"
            ,reply_markup=keyboard_district(message));
    else:
        bot.send_message(message.chat.id,"Hududni tanlang"
            ,reply_markup=keyboard_district(message));
    bot_register_next_step_handler(message,"checkDistrict");
def checkDistrict(message,text="_"):
    adr=state_read(message,"adres");
    if text=="_":
        text=message.text;
    if "Неизвестно" in adr:
        state(message,"adres",adr.replace("Неизвестно",text));
    else:
        if text not in adr:
            state(message,"adres",adr+" "+text);
    sender(message);
def cort_to_list(cort):
    list_ = [];
    for i in range(len(cort)):
        list_.append(cort[i][0]);
    return list_;
def get_address_from_coords(message,coords):
    try:
        PARAMS = {
            "apikey":"dcc7de33-5acb-4746-9558-a2bfbccc8391",
            "format":"json",
            "lang":"ru_RU",
            "kind":"house",
            "geocode": coords
        }
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]

        PARAMS = {
            "apikey":"dcc7de33-5acb-4746-9558-a2bfbccc8391",
            "format":"json",
            "lang":"ru_RU",
            "kind":"district",
            "geocode": coords
        }
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str2 = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]

        return address_str2#address_str+"\n"+address_str2
    except Exception as e:
        return "Адрес не установлен"
def sender(message):
    try:
        lat = state_read(message,"latitude")
        lon = state_read(message, "longitude")
        adres = state_read(message,"adres")
        lang = state_read(message,"lang")
        buf=state_read(message,"buf");
        if lat == "0":
            if adres == "🏃‍♂️Termoq" or adres == "🏃‍♂️Самовывоз":
                buf=buf+str("\n"+adres);
            else:
                buf=buf+str("\nАдрес: "+adres);

        else:
            file = open("adres/longitude.txt","r")
            x1 = file.read()
            file.close()
            file = open("adres/latitude.txt","r")
            y1 = file.read()
            file.close()

            x2 = state_read(message,"longitude")
            y2 = state_read(message,"latitude")

            #+++++++++++++++++++++++++++++
            X = (float(x1)-float(x2))
            X = X * X
            Y = (float(y1)-float(y2))
            Y = Y * Y
            S0 = X + Y
            S = math.sqrt(S0)
            file = open("S.txt","w")
            file.write("\n"+str(S))
            file.close()
            file = open("S.txt","r")
            S = file.read()
            file.close()
            S = round(float(S),5)
            km = S *100
            km = round(float(km),3)
            m = float(km)*1000
            m = round(int(m),0)


            Vcar = 50 #километров в час
            Vchel = 5 #километров в час

            #km = 50

            Tcar = 60*(km/Vcar)
            Tchel = 60*(km/Vchel)

            km = round(float(km),1)
            m = round(int(m),0)

            Tcar = round(int(Tcar),1)
            Tchel = round(int(Tchel),0)


            Tcarh = Tcar/60
            Tchelh = Tchel/60

            Tcarh = round(float(Tcarh),1)
            Tchelh = round(float(Tchelh),1)


            kmKoef = float(km)/3
            kmKoef = int(kmKoef)+int(km)

            if int(kmKoef)<=5:
                price_boss = 25000
            else:
                price_boss = (int(kmKoef)-5)*2000+10000
            price_boss = 25000#


            end_price = state_read(message,"end_price")
            new_saldo = int(end_price)+int(price_boss)

            if lang == "uz":
                buf=buf+str("\nManzil: "+adres);
            else:
                buf=buf+str("\nАдрес: "+adres);

            saldo_end = state_read(message,"end_price")
            state(message,"dostStr",str("\nС учетом доставки: "+str(int(saldo_end)+int(price_boss))))
            Z = []
            Z.append(lon)
            Z.append(lat)

        if adres == "🏃‍♂️Termoq" or adres == "🏃‍♂️Самовывоз":
            pass
        else:
            price_boss = 25000#
            saldo_end = state_read(message,"end_price")
            #state(message,"dostStr",str("\nС учетом доставки: "+str(int(saldo_end)+int(price_boss))))
        buf=buf+str("\nС учетом доставки: "+str(int(saldo_end)+int(price_boss)));
        data = state_read(message,"buf")
        bot.send_message(message.chat.id, data)
        if lat != "0":
            bot.send_location(message.chat.id,float(lat),float(lon))
        if lang == "ru":
            bot.send_message(message.chat.id, "Оставить комментарий к заказу?",reply_markup=keyboard_time(message))
        else:
            bot.send_message(message.chat.id, "Buyurtma uchun sharh qoldiringmi?",reply_markup=keyboard_time(message))
        state(message,'buf',buf);
        bot_register_next_step_handler(message,"get_time")
    except Exception as e:
        logger(message,e)
def get_time(message):
    try:
        lang = state_read(message,"lang")
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            basket(message)
        else:
            message_text = message.text;
            if message_text in DAYS:
                message_text="_";
            state(message,"time_del",str(message_text));
            if lang == "uz":
                bot.send_message(message.chat.id, "Yetkazib berish uchun haftaning bir kunini tanlang",reply_markup=keyboard_day_week(message))
            else:
                bot.send_message(message.chat.id, "Выберете день недели для доставки",reply_markup=keyboard_day_week(message))
            bot_register_next_step_handler(message,"get_day_del")
    except Exception as e:
        logger(message,e);
def get_day_del(message):
    try:
        lang = state_read(message,"lang")
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            basket(message)
        else:
            message_text = message.text;
            if message_text =="Dushanba":
                message_text = "Понедельник"
            elif message_text =="Chorshanba":
                message_text = "Вторник"
            elif message_text =="Seshanba":
                message_text = "Среда"
            elif message_text =="Payshanba":
                message_text = "Четверг"
            elif message_text =="Juma":
                message_text = "Пятница"
            elif message_text =="Shanba":
                message_text = "Суббота"
            elif message_text =="Yakshanba":
                message_text = "Воскресенье"
            #
            elif message.text in DAYS:
                try:
                    int(message.text)+1;
                    n=True;
                except:
                    n=False;
                if n:
                    message_text=message.text;
            #
            days_work=[]
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT day1 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Понедельник");
            cursor.execute("SELECT day2 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Вторник");
            cursor.execute("SELECT day3 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Среда");
            cursor.execute("SELECT day4 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Четверг");
            cursor.execute("SELECT day5 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Пятница");
            cursor.execute("SELECT day6 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Суббота");
            cursor.execute("SELECT day7 FROM days")
            day = cursor.fetchall()[0][0]
            if "✅" in day:
                days_work.append("Воскресенье");
            #
            z=22;
            for i in range(9):
                cursor.execute("SELECT day{0} FROM days".format(str(z)));

                day = cursor.fetchall()[0][0]
                if "✅" in day:
                    days_work.append(str(z));
                z+=1;
            #

            conn.close()
            if message_text in days_work:
                state(message,"day_week",str(message_text));
                if lang == "uz":
                    bot.send_message(message.chat.id, "ajoyib, buyurtma?",reply_markup=keyboard_pay_form(message))
                else:
                    bot.send_message(message.chat.id, "Выберете форму оплаты",reply_markup=keyboard_pay_form(message))
                bot_register_next_step_handler(message,"get_pay_form")
            else:
               # bot.send_message(message.chat.id, str(days_work),reply_markup=keyboard_day_week(message))
                bot.send_message(message.chat.id, "Неккоректный ввод",reply_markup=keyboard_day_week(message))

    except Exception as e:
        logger(message,e);
def get_pay_form(message):
    try:
        lang = state_read(message,"lang")
        if "Назад" in message.text or "Orqaga" in message.text:
            basket(message);
        else:
            if "PayMe" in message.text or "Click" in message.text or "Наличные" in message.text or "Naqd" in message.text:
                state(message,"pay_form",message.text);
                adres = state_read(message,"adres");
                if "🏃‍♂️" in adres:
                    if lang == "uz":
                        bot.send_message(message.chat.id, "Qo'shimcha telefon raqamingizni kiriting",reply_markup=keyboard_back(message))
                    else:
                        bot.send_message(message.chat.id, "Введите пожалуйста дополнительный номер телефона",reply_markup=keyboard_back(message))
                else:
                    if lang == "uz":
                        bot.send_message(message.chat.id, "Iltimos, manzilni matnga kiriting",reply_markup=keyboard_back(message))
                    else:
                        bot.send_message(message.chat.id, "Введите пожалуйста адрес текстом \n👉(Район, улица, номер дома, номер квартиры)👈",reply_markup=keyboard_back(message))
                bot_register_next_step_handler(message,"getTxtAdres")
            else:
                if lang == "uz":
                    bot.send_message(message.chat.id, "ajoyib, buyurtma?",reply_markup=keyboard_pay_form(message))
                else:
                    bot.send_message(message.chat.id, "Выберете форму оплаты",reply_markup=keyboard_pay_form(message))
                bot_register_next_step_handler(message,"get_pay_form")
    except Exception as e:
        logger(message,e);
def getTxtAdres(message):
    try:
        if "Назад" in message.text or "Orqaga" in message.text:
            basket(message);
        else:
            state(message,"txtAdres",message.text)
            if lang == "uz":
                bot.send_message(message.chat.id, "ajoyib, buyurtma?",reply_markup=keyboard_yes_no(message))
            else:
                bot.send_message(message.chat.id, "Как к вам обращаться? Введите контактное имя",reply_markup=keyboard_back(message))
            bot_register_next_step_handler(message,"getContactName")
    except Exception as e:
        logger(message,e);
def getContactName(message):
    try:
        if "Назад" in message.text or "Orqaga" in message.text:
            basket(message);
        else:
            state(message,"contactName",message.text)
            if lang == "uz":
                bot.send_message(message.chat.id, "ajoyib, buyurtma?",reply_markup=keyboard_yes_no(message))
            else:
                bot.send_message(message.chat.id, "Отлично, заказать?",reply_markup=keyboard_yes_no(message))
            bot_register_next_step_handler(message,"send")
    except Exception as e:
        logger(message,e);
def send(message):
    try:
        if message.text == "⬅️ Orqaga" or message.text == "⬅️ Назад":
            basket(message)
        elif message.text == "❌Yo'q" or message.text == "❌Нет":
            basket(message)
        elif message.text == "✅Ha" or message.text == "✅Да" or message.text == "Да":
            send_ok(message)
        else:
            start(message)
    except Exception as e:
        logger(message,e)
def checkDayWeek(day):
    message_text = day;
    if message_text =="Dushanba":
        message_text = "Понедельник"
    elif message_text =="Chorshanba":
        message_text = "Вторник"
    elif message_text =="Seshanba":
        message_text = "Среда"
    elif message_text =="Payshanba":
        message_text = "Четверг"
    elif message_text =="Juma":
        message_text = "Пятница"
    elif message_text =="Shanba":
        message_text = "Суббота"
    elif message_text =="Yakshanba":
        message_text = "Воскресенье"
    #
    elif day in DAYS:
        try:
            int(day)+1;
            n=True;
        except:
            n=False;
        if n:
            message_text=day;
    #
    days_work=[]
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT day1 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Понедельник");
    cursor.execute("SELECT day2 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Вторник");
    cursor.execute("SELECT day3 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Среда");
    cursor.execute("SELECT day4 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Четверг");
    cursor.execute("SELECT day5 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Пятница");
    cursor.execute("SELECT day6 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Суббота");
    cursor.execute("SELECT day7 FROM days")
    day = cursor.fetchall()[0][0]
    if "✅" in day:
        days_work.append("Воскресенье");
    #
    z=22;
    for i in range(9):
        cursor.execute("SELECT day{0} FROM days".format(str(z)));
        day = cursor.fetchall()[0][0]
        if "✅" in day:
            days_work.append(str(z));
        z+=1;
    #
    conn.close();
    print(days_work);
    if message_text in days_work:
        var=True;
    else:
        var=False;
    return var
def send_ok(message):
    try:
        lang = state_read(message,"lang")
        adres = state_read(message,"adres")
        lon = state_read(message,"longitude")
        lat = state_read(message,"latitude")
        contact = state_read(message,"contact")
        time_del = state_read(message,"time_del")
        day_week = state_read(message,"day_week")
        txtAdres = state_read(message,"txtAdres")
        contactName = state_read(message,"contactName")
        buf=state_read(message,'buf');
        if checkDayWeek(day_week):
            print("allCorrect in DAYS")
        else:
            print("Problem in DAYS!")
            bot.send_message(message.chat.id, "Произошли изменения и выбранный день сейчас неактивен. Извините за неудобства");
            basket(message);
            return "";
        try:
            dostStr = state_read(message,"dostStr")
        except:
            dostStr = ""
        try:
            pay_form = state_read(message,"pay_form")
        except:
            pay_form = "?";

        file = open("last_index.txt","r")
        last_index = file.read()
        file.close()
        last_index = int(last_index)+1
        if len(str(last_index))==1:
            last_index = "000"+str(last_index)
        if len(str(last_index))==2:
            last_index = "00"+str(last_index)
        if len(str(last_index))==3:
            last_index = "0"+str(last_index)
        else:
            last_index=str(last_index);
        file = open("last_index.txt","w")
        file.write(str(last_index))
        file.close()

        buf=buf+"\nНомер: "+ str(contact)
        buf=buf+"\nКонтактное имя: "+contactName
        buf=buf+"\n"+dostStr
        buf=buf+"\nКомментарий: "+str(time_del)
        buf=buf+"\nАдрес текстом: "+str(txtAdres)
        buf=buf+"\nФорма оплаты: "+str(pay_form)
        buf=buf+"\nДень недели: "+str(day_week)

        buf=buf+str("\n\nНомер заказа: "+str(last_index))

        state(message,'buf',buf);
        resu=base("SELECT chat_id FROM all_stat WHERE chat_id = '{0}'".format(str(message.chat.id),))
        if len(resu)==0:
            buf=buf+str("\nНовичок🔥")

        data = state_read(message,"buf").replace("Корзина:","Номер заказа: "+str(last_index))

        #
        bask=bask_show(message);
        print(bask);
        jsonData=json.dumps(bask);
        #
        day=dayFromTxt(data);
        district=get_district(adres);
        new_order_add(message,contact,adres,data,last_index,jsonData,lon,lat,day,district)
        bot.send_message(channel, data, reply_markup=keyboard_accept(message,last_index))
        if lat != "0":
            bot.send_location(channel,float(lat),float(lon),reply_markup=keyboard_del_loc(message));

        if lang == "uz":
            bot.send_message(message.chat.id,"Rahmat, sizning buyurtmangiz qayta ishlash uchun yuborildi. Buyurtma raqami: "+str(last_index))
        else:
            bot.send_message(message.chat.id,"Спасибо за заказ, после проверки Вам придет уведомление\nНомер заказа: "+str(last_index))
        state_del(message,str("contact"))
        state_del(message,str("latitude"))
        state_del(message,str("longitude"))
        state_del(message,str("adres"))
        basket_del_all(message)
        path_rem_all(message)
        start(message)
    except Exception as e:
        logger(message,e)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        # Если сообщение из чата с ботом
        message = call.message
        current_datetime = datetime.now()
        if False:#DEBUG == True and message.chat.id != 104932971:
            bot.answer_callback_query(callback_query_id=call.id, text="Технические работы", show_alert=False)
        else:
            if call.message:
                #channel_drivers = str(message.chat.id)
                if call.data == "edit_this":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message.text+"\nsome")
                if "ID" in call.data:
                    data = call.data.replace("ID","")
                    print(data)
                    conn = sqlite3.connect('db.sqlite')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product SET work = '1' WHERE id = '"+str(data)+"'")
                    conn.commit()
                    conn.close()
                    bot.send_message(message.chat.id,"Товар включен")

                if "remove_location" in call.data:
                    bot.delete_message(message.chat.id, message.message_id)

                if "no" in call.data:
                    last_index = call.data.replace("no","")
                    del_id=db("SELECT tg_id FROM orders WHERE num = '{0}'".format(last_index,))[0];
                    db("DELETE FROM orders WHERE num = '{0}'".format(last_index));
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(message.text)+"\n\nОтклонено❌",reply_markup=keyboard_cancel_option(message,del_id))
                    
                if "option" in call.data:
                    if "option1" in call.data:
                        del_id = call.data.replace("option1","");
                        txt='Неверно указан номер телефона';
                    elif "option2" in call.data:
                        del_id = call.data.replace("option2","");
                        txt='Не указан узбекский номер телефона';
                    elif "option3" in call.data:
                        del_id = call.data.replace("option3","");
                        txt='Свяжитесь с администратором группы';
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(message.text)+"\n"+txt);
                    bot.send_message(del_id, "Ваш заказ был отклонен, причина: "+txt);
                    
                if "accept" in call.data:
                    hour = int(current_datetime.hour)
                    last_index = call.data.replace("accept","")
                    del_id=db("SELECT tg_id FROM orders WHERE num = '{0}'".format(last_index,))[0];
                    data = call.message.text;
                    statistic_write(message,data,del_id);
                    db("UPDATE orders SET status='1' WHERE num = '{0}'".format(last_index));
                    day = dayFromTxt(data);
                    district=get_district(data);
                    ind=indCount(data);
                    indu=indCount(data,"Индоутка");
                    gus=indCount(data,"Гусь");
                    allInd=str(int(indAllF(day))+int(ind));
                    allIndu=str(int(indAllF(day,2))+int(indu));
                    allGus=str(int(indAllF(day,3))+int(gus));
                    print(ind,indu,gus,'<<<<');
                    db("UPDATE orders SET ind={0} WHERE num = '{1}'".format(ind,last_index));
                    db("UPDATE orders SET indu={0} WHERE num = '{1}'".format(indu,last_index));
                    db("UPDATE orders SET gus={0} WHERE num = '{1}'".format(gus,last_index));
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(message.text)+"\n\n✅Принято✅")
                    ccaSum=parse_order_amount(db("SELECT basket FROM orders WHERE num ='{0}'".format(last_index,))[0]);
                    allccaSum=ccaSum;
                    price_boss=25000;
                    ccaSum=str(int(ccaSum)-price_boss);
                    bot.send_message(del_id,"Ваш заказ принят!\nНомер заказа: {0}\nДень: {1}\nПРИМЕРНАЯ СУММА: {2}\nДоставка: {3}\nИТОГО: {4}".format(last_index,day,ccaSum,price_boss,allccaSum));
                    howManyDistr=str(len(db("SELECT id FROM orders WHERE status = '1' AND district = '{0}'".format(district,))));
                    howManyDay=str(len(db("SELECT id FROM orders WHERE status = '1' AND day = '{0}'".format(day,))));
                    bot.send_message(message.chat.id,'В базе "{0}" есть {1} заказ(a/ов)\nНа район {2} приходится {3} заказ(a/ов)\nДанный заказ содержит {4} инде(йки/ек)\nВсего индеек в базе "{0}" : {5}\nВсего индоуток в базе "{0}" : {6}\nВсего гусей в базе "{0}" : {7}'.format(day,howManyDay,district,howManyDistr,ind,allInd,allIndu,allGus));
                    if int(howManyDay)>=MAX_ORDERS:
                        db("UPDATE days SET '{0}' = '❌'".format(dayToBase(day)));
                        bot.send_message(message.chat.id,"База "+day+" была заполнена на "+str(MAX_ORDERS)+" И была закрыта");

                if "day" in call.data:
                    if "dayClose" in call.data:
                        bot.delete_message(message.chat.id, message.message_id);
                    else:
                        bot.delete_message(message.chat.id, message.message_id);
                        bot.send_message(message.chat.id,"Выберете день",reply_markup=keyboard_inline_days(message));
                        send_day_orders(message,call.data);
                if "get_location" in call.data:
                    last_index = call.data.replace("get_location","");
                    lon=db("SELECT lon FROM orders WHERE num = '{0}'".format(last_index,))[0];
                    lat=db("SELECT lat FROM orders WHERE num = '{0}'".format(last_index,))[0];
                    if lat != "0":
                        bot.send_location(channel_drivers,float(lat),float(lon));
                if "order_done" in call.data:
                    last_index = call.data.replace("order_done","");
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(message.text)+"\n\n✅Доставлено✅")
                    bot.send_message(channel,"Заказ номер: "+last_index+" - Доставлен");
                    db("UPDATE orders SET status = '3' WHERE num = '{0}'".format(last_index,));


    except Exception as e:
        logger(message,e)



#+++++++++++++функционал++++++
def parse_order_amount(text):
    import re
    match = re.search(r'С учетом доставки: (\d+)', text)
    if match:
        return str(match.group(1))
    else:
        return None;

def dayToBase(data):
    if "Понедельник" in data or "Dushanba" in data:
        base = "day1";
    elif "Вторник" in data or "Seshanba" in data:
        base = "day2";
    elif "Среда" in data or "Chorshanba" in data:
        base = "day3";
    elif "Четверг" in data or "Payshanba" in data:
        base = "day4";
    elif "Пятница" in data or "Juma" in data:
        base = "day5";
    elif "Суббота" in data or "Shanba" in data:
        base = "day6";
    elif "Воскресенье" in data or "Yakshanba" in data:
        base = "day7";
    return base;
def indAllF(day,bird=1):
    allInd=0;
    if bird==1:
        indList=db("SELECT ind FROM orders WHERE status = '1' AND day = '{0}'".format(day));
    elif bird==2:
        indList=db("SELECT indu FROM orders WHERE status = '1' AND day = '{0}'".format(day));
    elif bird==3:
        indList=db("SELECT gus FROM orders WHERE status = '1' AND day = '{0}'".format(day));
    for i in indList:
        allInd=allInd+int(i);
    return allInd;
def indCount(txt,search="Индейка"):
    file=open("buf.txt","w");
    file.write(txt);
    file.close();
    file=open("buf.txt","r");
    lines=file.readlines();
    file.close();
    ind=0;
    indAll=0;
    for i in range(len(lines)):
        line=lines[i]
        if search in line:
            ind+=1;
            howLine=lines[i+1];
            howD="";
            for z in range(len(howLine)):
                if howLine[z]=="x":
                    howD=howD.replace(" ","");
                    indAll+=int(howD);
                    break;
                else:
                    howD+=howLine[z];
    return indAll;

def get_district(adres):
    adres=adres.lower();

    if "хонт" in adres or "хант" in adres:
        district="Шайхантахур";
    elif "ирз" in adres:
        district="Мирзо-Улугбек";
    elif "лма" in adres:
        district="Алмазар";
    elif "нус" in adres:
        district="Юнус-Абад";
    elif "сара" in adres:
        district="Яккасарай";
    elif "шна" in adres:
        district="Яшнабад";
    elif "уйл" in adres:
        district="Куйлюк";
    elif "ект" in adres:
        district="Бектемир";
    elif "ерг" in adres:
        district="Сергели";
    elif "ила" in adres:
        district="Чиланзар";
    elif "мир" in adres:
        district="Мирабад";
    elif "учте" in adres:
        district="Учтепа";
    else:
        district="Неизвестно";
    return district;
def dayFromTxt(data):
    if "Понедельник" in data or "Dushanba" in data:
        base = "Понедельник";
    elif "Вторник" in data or "Seshanba" in data:
        base = "Вторник";
    elif "Среда" in data or "Chorshanba" in data:
        base = "Среда";
    elif "Четверг" in data or "Payshanba" in data:
        base = "Четверг";
    elif "Пятница" in data or "Juma" in data:
        base = "Пятница";
    elif "Суббота" in data or "Shanba" in data:
        base = "Суббота";
    elif "Воскресенье" in data or "Yakshanba" in data:
        base = "Воскресенье";
    else:
        file=open("dayBuf.txt","w");
        file.write(data);
        file.close();
        file=open("dayBuf.txt","r");
        lines=file.readlines();
        file.close();
        for l in lines:
            if "День недели: "in l:
                day=l.replace("День недели: ","").replace(" ","").replace("\n","");
                break;
        base=day;
        os.remove("dayBuf.txt");
    return base;
'''
def save_order(message,data,lon,lat):
    try:
        conn = sqlite3.connect('days.sqlite')
        cursor = conn.cursor()
        if "Понедельник" in data or "Dushanba" in data:
            base = "day1";
        elif "Вторник" in data or "Seshanba" in data:
            base = "day2";
        elif "Среда" in data or "Chorshanba" in data:
            base = "day3";
        elif "Четверг" in data or "Payshanba" in data:
            base = "day4";
        elif "Пятница" in data or "Juma" in data:
            base = "day5";
        elif "Суббота" in data or "Shanba" in data:
            base = "day6";
        elif "Воскресенье" in data or "Yakshanba" in data:
            base = "day7";
        else:
            file=open("dayBuf.txt","w");
            file.write(data);
            file.close();
            file=open("dayBuf.txt","r");
            lines=file.readlines();
            file.close();
            for l in lines:
                if "День недели: "in l:
                    day=l.replace("День недели: ","").replace(" ","").replace("\n","");
                    break;
            base="day"+day;
            os.remove("dayBuf.txt");
        cdo=countDistrictOrder(data);
      
        distrCount=cdo['count'];
        distr=cdo['distr'];
        file = open("lIndex","w");
        file.write(data);
        file.close();
        file = open("lIndex","r");
        lIndexData = file.readlines();
        file.close();
        for string in lIndexData:
            if "Номер заказа: " in string:
                last_index = string.replace("Номер заказа: ","")
        cursor.execute("SELECT id FROM '"+base+"'")
        index = str(len(cursor.fetchall())+1);
        cursor.execute("INSERT INTO {0} VALUES((?),(?),(?),(?),(?))".format(base,),(index,data,lon,lat,last_index))
        conn.commit()
        cursor.execute("SELECT id FROM '"+base+"'");
        index = len(cursor.fetchall());
        cursor.execute("SELECT data FROM '"+base+"'");
        datas = cursor.fetchall();
        d="";
        for i in range(len(datas)):
            d=d+"\n"+datas[i][0];
        conn.close()
        file=open("buf.txt","w");
        file.write(d);
        file.close();
        file=open("buf.txt","r");
        lines=file.readlines();
        file.close();
        ind=0;
        indAll=0;
        for i in range(len(lines)):
            line=lines[i]
            if "Индейка" in line:
                ind+=1;
                howLine=lines[i+1];
                howD="";
                for z in range(len(howLine)):
                    if howLine[z]=="x":
                        howD=howD.replace(" ","");
                        indAll+=int(howD);
                        break;
                    else:
                        howD+=howLine[z];


        baseTxt=base;
        if '1' in base:
            baseTxt='"Понедельник"';
        elif '2' in base:
            baseTxt='"Вторник"';
        elif '3' in base:
            baseTxt='"Среда"';
        elif '4' in base:
            baseTxt='"Четверг"';
        elif '5' in base:
            baseTxt='"Пятница"';
        elif '6' in base:
            baseTxt='"Суббота"';
        elif '7' in base:
            baseTxt='"Воскресенье"';

        bot.send_message(message.chat.id,"В базе "+baseTxt+" есть "+str(ind)+" заказов содержащих индейку\nВсего индеек в данной базе: "+str(indAll));
        if index>=MAX_ORDERS:
            conn = sqlite3.connect('db.sqlite');
            cursor = conn.cursor();
            cursor.execute("UPDATE days SET '{0}' = '❌'".format(base));

            bot.send_message(message.chat.id,"База "+baseTxt+" была заполнена на "+str(MAX_ORDERS)+" И была закрыта");
            conn.commit();
            conn.close();
        else:
            bot.send_message(message.chat.id,"В базе "+baseTxt+" теперь "+str(index)+" заказов");
            bot.send_message(message.chat.id,"В базе района "+distr+" теперь "+str(distrCount)+" заказов");



    except Exception as e:
        logger(message,e);
'''
def countDistrictOrder(data):
    ret={};
    ret['distr']=get_district(data);
    print(ret,'<<<<<')
    count=0;
    for t in Tables:
        datas=basic_db("SELECT data FROM "+t);
        for d in datas:
            print(">>>",ret['distr'],"\n>>>",d);
            if ret['distr'] in d:
                count+=1;
    ret['count']=str(count);
    return ret;
def distance(Z,marsh_list):
    Ax = float(marsh_list[0][0])
    Ay = float(marsh_list[1][0])
    Bx = float(marsh_list[2][0])
    By = float(marsh_list[3][0])
    marsh_name = marsh_list[4][0]
    print(
        "Ax > "+str(Ax)
        +"\nAy > "+str(Ay)
        +"\nBx > "+str(Bx)
        +"\nBy > "+str(By)
        +"\n\nZ > "+str(Z)
        )
    if Ax < Bx:
        a1 = Ax
        b1 = Bx
        Bx = a1
        Ax = b1
    if Ay < By:
        a1 = Ay
        b1 = By
        By = a1
        Ay = b1
    first = []
    while Bx <= Ax:
        first.append(Bx)
        Bx = Bx + 1
    var = Ay - By
    try:
        koef = var/len(first)
    except:
        koef = 0
    second = []
    for i in range(len(first)):
        By = By + koef
        second.append(By)
    metr_list = []
    for i in range(len(first)):
        print("("+str(first[i])+","+str(second[i])+")")
        metr = dist(first[i],second[i],Z[0],Z[1])
        metr_list.append(metr)
    min_metr = min(metr_list)
    for i in range(len(metr_list)):
        if metr_list[i] == min_metr:
            this = [first[i],second[i],marsh_name]
            break
    return this
def dist(x2,y2,x1,y1):
    X = (float(x1)-float(x2))
    X = X * X
    Y = (float(y1)-float(y2))
    Y = Y * Y
    S0 = X + Y
    S = math.sqrt(S0)
    file = open("S.txt","w")
    file.write("\n"+str(S))
    file.close()
    file = open("S.txt","r")
    S = file.read()
    file.close()
    S = round(float(S),5)
    km = S *100
    km = round(float(km),3)
    m = float(km)*1000
    m = round(int(m),0)

    km = round(float(km),1)
    m = round(int(m),0)
    return m
def find_in_all(Z):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT A FROM locations ")
    A = cursor.fetchall()
    cursor.execute("SELECT B FROM locations ")
    B = cursor.fetchall()
    cursor.execute("SELECT C FROM locations ")
    C = cursor.fetchall()
    cursor.execute("SELECT D FROM locations ")
    D = cursor.fetchall()
    cursor.execute("SELECT E FROM locations ")
    E = cursor.fetchall()
    cursor.execute("SELECT F FROM locations ")
    F = cursor.fetchall()

    #A = [1,1,5,5,"A"]
    #B = [3,1,9,1,"B"]
    #C = [5,2,9,6,"C"]
    #D = [10,1,10,7,"D"]
    #E = [6,5,2,9,"E"]
    #F = [3,5,3,10,"F"]
    conn.close()
    marsh_list = [A,B,C,D,E,F]
    short_list = []
    short_name = []
    for i in range(len(marsh_list)):
        koor = distance(Z,marsh_list[i])
        short = dist(koor[0],koor[1],Z[0],Z[1])
        short_list.append(short)
        short_name.append(koor[2][0])
    for i in range(len(short_list)):
        if short_list[i] == min(short_list):
            print("short in all >> "+str(short_name[i]))
            shortest = short_name[i]
    return shortest
def statistic_read(time_var):
    data = ""
    saldo = 0
    slices = []
    activities = []
    activities2 = []
    saldos = []
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    if time_var == "day":
        cursor.execute("SELECT how_many FROM day_stat");
    elif time_var == "month":
        cursor.execute("SELECT how_many FROM month_stat");
    elif time_var == "all":
        cursor.execute("SELECT how_many FROM all_stat");
    id_stat = cursor.fetchall();
    how_many_all = 0;
    for how in id_stat:
        how_many_all+=int(how[0]);
    data+="\nВсего продано "+str(how_many_all)+" единиц(ы) товара"
    if time_var == "day":
        cursor.execute("SELECT price FROM day_stat");
    elif time_var == "month":
        cursor.execute("SELECT price FROM month_stat");
    elif time_var == "all":
        cursor.execute("SELECT price FROM all_stat");
    prices = cursor.fetchall()
    for price in prices:
        saldo += int(price[0])
    data+="\nВсего продано на сумму "+str(saldo)+" сум"
    if time_var == "day":
        cursor.execute("SELECT cat_name FROM day_stat")
    elif time_var == "month":
        cursor.execute("SELECT cat_name FROM month_stat")
    elif time_var == "all":
        cursor.execute("SELECT cat_name FROM all_stat")
    cat_name = cursor.fetchall()
    cat_name_list = []
    for i in range(len(cat_name)):
        if cat_name[i][0] not in  cat_name_list:
            cat_name_list.append(cat_name[i][0])
    for i in range(len(cat_name_list)):
        if time_var == "day":
            cursor.execute("SELECT price FROM day_stat WHERE cat_name = '"+str(cat_name_list[i])+"'")
        elif time_var == "month":
            cursor.execute("SELECT price FROM month_stat WHERE cat_name = '"+str(cat_name_list[i])+"'")
        elif time_var == "all":
            cursor.execute("SELECT price FROM all_stat WHERE cat_name = '"+str(cat_name_list[i])+"'")
        prices = cursor.fetchall()

        if time_var == "day":
            cursor.execute("SELECT how_many FROM day_stat WHERE cat_name = '"+str(cat_name_list[i])+"'")
        elif time_var == "month":
            cursor.execute("SELECT how_many FROM month_stat WHERE cat_name = '"+str(cat_name_list[i])+"'")
        elif time_var == "all":
            cursor.execute("SELECT how_many FROM all_stat WHERE cat_name = '"+str(cat_name_list[i])+"'")
        how_many_list = cursor.fetchall()
        how_many = 0;
        for how in how_many_list:
            how_many+=int(how[0]);

        slices.append(how_many)
        price_cat_name = 0
        for z in range(len(prices)):
            price_cat_name+=int(prices[z][0])
        activities.append(cat_name_list[i]+"\n"+str(price_cat_name))
        saldos.append(price_cat_name)

    for i in range(len(cat_name_list)):
        data+="\n"+cat_name_list[i]+" продано: "+str(slices[i])+"шт\nНа сумму: "+str(saldos[i])+" сум"
        activities2.append(cat_name_list[i]+"- "+str(slices[i])+"шт")


    plt.gcf().clear()
    slices = [aSlice/max(slices) for aSlice in slices]
    plt.pie(slices,labels=activities2,autopct='%1.1f%%',startangle=140)
    plt.savefig("graph")
    #plt.show()
    plt.gcf().clear()
    saldos = [aSlice2/max(saldos) for aSlice2 in saldos]
    plt.pie(saldos,labels=activities,autopct='%1.1f%%',startangle=140)
    plt.savefig("graph_price")
    #plt.show()


    print(data)
    conn.close()
    return data
def new_order_add(message,contact,adres,data,last_index,jsonData,lon,lat,day,district):
    try:
        time = str(datetime.now())
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders")
        results = cursor.fetchall()
        index = str(len(results)+1)
        status = '0'
        name = str(message.from_user.username)
        tg_id = str(message.chat.id)
        cursor.execute("INSERT INTO orders VALUES((?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?))",(index,status,name,tg_id,contact,adres,data,time,last_index,jsonData,lon,lat,day,district,"0","0","0",))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def new_order_list(message,data,lon,lat,driver,last_index):
    try:
        conn = sqlite3.connect('loc.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM '"+driver+"'")
        results = cursor.fetchall()
        index = str(len(results)+1)
        cursor.execute("INSERT INTO "+driver+" VALUES((?),(?),(?),(?),(?))",(index,data,lon,lat,last_index))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
testDel = '''
Корзина:
№4  | Куры🍗
2 x 1000 = 2000
№5  | Куры🍗
2 x 1000 = 2000
№1  | Голень🍗
3 x 1000 = 3000
№2  | Голень🍗
2 x 1000 = 2000
№3  | Голень🍗
5 x 1000 = 5000
№6  | Куры123🍗
2 x 1000 = 2000


Итого: 0 сум
🏃‍♂️Самовывоз
Номер: +998908084985
Комментарий: Без комментария
Форма оплаты: Наличные
День недели: Суббота

Номер заказа: 0015
'''
#+++++++++++++функционал++++++
def stringParser(message,text):
    try:
        os.remove("nak.txt")
    except:
        pass
    try:
        os.remove("nak2.txt")
    except:
        pass
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM category")
    cats1 = cursor.fetchall()
    cursor.execute("SELECT name_uz FROM category")
    cats2 = cursor.fetchall()
    cats = cats1+cats2
    file = open("days.txt","w")
    file.write(text)
    file.close()
    file = open("days.txt","r")
    strings = file.readlines()
    file.close()
    conn.close()
    Mass = []
    allPrice="0";
    for i in range(len(strings)):
        string = strings[i].replace("\n","");
        if "№" in string:
            num = "";
            for z in range(len(string)):
                if string[z] == " ":
                    num+=string[z];
                    break;
                else:
                    num+=string[z]; #получение номера позиции с пробелом;
            string = string.replace(num,"");
            price="0";
            for cat in cats:
                if cat[0] in string:
                    Cat = cat[0];
                    Prod = string.replace(cat[0]+" ","").replace(" | ",""); #Разделение на категорию и товар
                    price=str(get_price(Prod));
                    allPrice=str(int(allPrice)+int(price));
                    cat_prod = Cat+" "+Prod;
                    break;
            eqString = strings[i+1].replace("\n","");
            saldo = "";
            saldo = saldo.replace(" ","");
            saldo = saldo.replace("=","");
            for z in range(len(eqString)): #получение итоговой суммы
                if eqString[z]=="=":
                    saldo = "";
                if eqString[z]=="x":
                    how_many = saldo.replace(" ","");
                else:
                    saldo+=eqString[z];
            saldo = saldo.replace("= ","");
            try:
                file = open("nak.txt","r")
                nak = file.read()
                file.close()
            except:
                nak = "";
            nak = "№"+cat_prod+"*"+how_many+"\n";
            file = open("nak.txt","a")
            file.write(nak)
            file.close()

            nak = "№"+cat_prod+"*"+how_many+" = "+price+"\n";
            file = open("nak2.txt","a")
            file.write(nak)
            file.close()




    file = open("nak.txt","r")
    nak = file.read()
    file.close()
    print(nak+"\n")
    file = open("nak.txt","r")
    nakList = file.readlines()
    file.close()
    clearList = []
    clearCort = {}
    for string in nakList:
        string = string.replace("\n","");
        for s in range(len(string)):
            if string[s] == "*":
                pos = string[:s]
                how_many = string[s+1:]
                #print(pos)
                #print(how_many)
                if pos not in clearList:
                    clearList.append(pos);
                    clearCort[pos]=how_many
                else:
                    old = int(clearCort[pos])+int(how_many);
                    clearCort[pos]=str(old)
    res = ""
    for pos in clearCort:
        res=res+pos+"*"+clearCort[pos]+"\n"
    file = open("days.txt","w");
    file.write(res);
    file.close();
    file = open("days.txt","r");
    strings = file.readlines();
    file.close();
    os.remove("days.txt");
    howManyAll = 0;
    for i in range(len(strings)):
        if "№"in strings[i]:
            line = strings[i];
            for z in range(len(line)):
                if line[z]=="*":
                    how = int(line[z+1:]);
                    howManyAll +=how;
    #file = open("nak2.txt","r");
    #res = file.read();
    #file.close();
    res = res+"\n\nВсего единиц товара: "+str(howManyAll);
    res = res+"\nОбщая сумма: "+str(allPrice);
    return res
def statistic_write(message,text,chat_id='_'):
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM category")
        cats1 = cursor.fetchall()
        cursor.execute("SELECT name_uz FROM category")
        cats2 = cursor.fetchall()
        cats = cats1+cats2
        file = open("stat","w")
        file.write(text)
        file.close()
        file = open("stat","r")
        strings = file.readlines()
        file.close()
        conn.close()
        time = str(datetime.now())
        for i in range(len(strings)):
            string = strings[i].replace("\n","");
            if "№" in string:
                num = "";
                for z in range(len(string)):
                    if string[z] == " ":
                        num+=string[z];
                        break;
                    else:
                        num+=string[z]; #получение номера позиции с пробелом;
                string = string.replace(num,"");
                for cat in cats:
                    if cat[0] in string:
                        Cat = cat[0];
                        Prod = string.replace(cat[0]+" ",""); #Разделение на категорию и товар
                        cat_prod = Cat+" "+Prod;
                        break;
                eqString = strings[i+1].replace("\n","");
                saldo = "";
                for z in range(len(eqString)): #получение итоговой суммы
                    if eqString[z]=="=":
                        saldo = "";
                    if eqString[z]=="x":
                        how_many = saldo.replace(" ","");
                    else:
                        saldo+=eqString[z];
                saldo = saldo.replace(" ","");
                saldo = saldo.replace("=","");
                conn = sqlite3.connect('db.sqlite')
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM day_stat")
                index = str(len(cursor.fetchall())+1);
                cursor.execute("INSERT INTO day_stat VALUES((?),(?),(?),(?),(?),(?),(?))",(index,Cat,Prod,cat_prod,saldo,time,how_many))

                cursor.execute("SELECT id FROM month_stat")
                index = str(len(cursor.fetchall())+1);
                cursor.execute("INSERT INTO month_stat VALUES((?),(?),(?),(?),(?),(?),(?))",(index,Cat,Prod,cat_prod,saldo,time,how_many))

                cursor.execute("SELECT id FROM all_stat")
                index = str(len(cursor.fetchall())+1);
                cursor.execute("INSERT INTO all_stat VALUES((?),(?),(?),(?),(?),(?),(?),(?))",(index,Cat,Prod,cat_prod,saldo,time,how_many,str(chat_id)))

                conn.commit()
                conn.close()
    except Exception as e:
        logger(message,e)
def clear_alfa(text,how_many):
    try:
        print("???")
        print(text)
        t = ""
        text = text[-3:]
        text = text.replace(",",".")
        if "." not in text:
            try:
                int(text[0])+1
                t =t + text[0]
            except:
                pass
            try:
                int(text[1])+1
                t = t + text[1]
            except:
                pass
            t = t + text[2]
            text = t
        print(text)
        print("???")
        text = text.replace(" ","")
        text = float(text)*int(how_many)
        return text
    except Exception as e:
        print(e)
def path_read(message):
    try:
        chat_id = str(message.chat.id)
        conn = sqlite3.connect("users/"+chat_id+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM path")
        results = cursor.fetchall()
        conn.close()
        path = []
        for i in range(len(results)):
            path.append(results[i][0])
        return path
    except Exception as e:
        logger(message,e)
def new_path(message,new):
    try:
        chat_id = str(message.chat.id)
        conn = sqlite3.connect("users/"+chat_id+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM path")
        results = cursor.fetchall()
        index = str(len(results)+1)
        cursor.execute("INSERT INTO path VALUES((?),(?))",(index,new))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def path_rem(message):
    try:
        chat_id = str(message.chat.id)
        conn = sqlite3.connect("users/"+chat_id+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM path")
        results = cursor.fetchall()
        place = str(len(results))
        cursor.execute('''DELETE FROM path WHERE id = ?''',(place,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def path_rem_all(message):
    try:
        chat_id = str(message.chat.id)
        conn = sqlite3.connect("users/"+chat_id+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM path")
        results = cursor.fetchall()
        for i in range(len(results)):
            place = i+1
            cursor.execute('''DELETE FROM path WHERE id = ?''',(place,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def bot_register_next_step_handler(message, func):
    try:
        state(message,"step",func)
        #file = open("steps/"+str(message.chat.id)+".txt","w")
        #file.write(func)
        #file.close()
    except Exception as e:
        logger(message,e)
def base(command):
    conn = sqlite3.connect("db.sqlite");
    cursor = conn.cursor();
    data='0';
    if "SELECT" in command:
        cursor.execute(command);
        data = cort_to_list(cursor.fetchall());
    elif "UPDATE" in command  or "INSERT" in command or "DELETE" in command:
        cursor.execute(command);
        conn.commit();
    elif "CREATE TABLE" in command or "DROP TABLE" in command:
        cursor.execute(command);
        conn.commit();
    conn.close();
    return data;
def logger(message,e):
    logging.error(e)
    file = open("log/mylog.txt","w")
    file.write(traceback.format_exc())
    file.close()
    #file = open("log/mylog2.txt","a")
    #file.write(traceback.format_exc())
    #file.close()
    file = open("err.txt","w")
    file.write("1")
    file.close()
    file = open("log/mylog.txt","r")
    data = file.read()
    file.close()

    bot.send_message(104932971,data);
    #restart(message)
def logger1(e):
    logging.error(e)
    file = open("log/mylog.txt","w")
    file.write(traceback.format_exc())
    file.close()
    file = open("err.txt","w")
    file.write("1")
    file.close()
    file = open("log/mylog.txt","r")
    data = file.read()
    file.close()
#+++++++sql
def basic_db(command):
    conn = sqlite3.connect("days.sqlite");
    cursor = conn.cursor();
    data='0';
    if "SELECT" in command:
        cursor.execute(command);
        data = cort_to_list(cursor.fetchall());
    elif "UPDATE" in command  or "INSERT" in command or "DELETE" in command:
        cursor.execute(command);
        conn.commit();
    conn.close();
    return data;
def db(command):
    conn = sqlite3.connect("db.sqlite");
    cursor = conn.cursor();
    data='0';
    if "SELECT" in command:
        cursor.execute(command);
        data = cort_to_list(cursor.fetchall());
    elif "UPDATE" in command  or "INSERT" in command or "DELETE" in command:
        cursor.execute(command);
        conn.commit();
    conn.close();
    return data;
def db_new_user(message):
    try:
        chat_id = message.chat.id
        file=open("users/"+str(chat_id)+".sqlite","w")
        file.write("")
        file.close()
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE 'states' (key TEXT, value TEXT)")
        cursor.execute("CREATE TABLE 'basket' (name TEXT, price TEXT, how_many TEXT)")
        cursor.execute("CREATE TABLE 'path' (id TEXT, value TEXT)")
        conn.commit()
        conn.close();
    except Exception as e:
        logger(message,e)
def state(message,place,insert):
    try:
        chat_id = message.chat.id
        try:
            insert = insert.replace("'","`").replace('"','``')
            place = place.replace("'","`").replace('"','``')
        except:
            pass
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        table = "states"
        column = str(place)
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM states WHERE key = '"+str(place)+"'")
        results = cursor.fetchall()
        if len(results) == 0:
            cursor.execute("INSERT INTO states VALUES('"+str(place)+"','"+str(insert)+"')")
        else:
            cursor.execute("UPDATE states SET value = '"+str(insert)+"' WHERE key = '"+str(place)+"'")
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def state_read(message,place):
    chat_id = message.chat.id
    conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM states WHERE key = '"+str(place)+"'")
    results = cursor.fetchall()
    conn.close()
    str_files = results[0][0]
    return str_files
def get_price(prod):
    conn = sqlite3.connect('db.sqlite');
    cursor = conn.cursor();
    print(prod)
    cursor.execute("SELECT name FROM product");
    names = cursor.fetchall();
    for i in range(len(names)):
        print(names[i][0],'<<<',prod);
        if names[i][0] in prod:
            cursor.execute("SELECT id FROM product WHERE name='{0}'".format(names[i][0]));
            prod_id = cursor.fetchall()[0][0];
            break;
    try:
        cursor.execute("SELECT price FROM product WHERE id ={0}".format(prod_id));
        price = cursor.fetchall()[0][0];
    except:
        price='0';
        print('error price','prod_id=0');
    conn.close();
    return price;
def get_how_many(message,place):
    chat_id = message.chat.id
    conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT how_many FROM basket WHERE name = '"+str(place)+"'")
    results = cursor.fetchall()
    conn.close()
    str_files = results[0][0]
    return str_files
def state_del(message,place):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM states WHERE key = ?''',(place,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def get_cat_id(message,name):
    try:
        lang = state_read(message,"lang")
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        if lang == "ru":
            cursor.execute("SELECT id FROM category WHERE name = '"+str(name)+"'");
        else:
            cursor.execute("SELECT id FROM category WHERE name_uz = '"+str(name)+"'");
        results = cursor.fetchall()
        conn.close()
        return results[0][0]
    except Exception as e:
        logger(message,e)
def get_cat_id_for_cat(message,name):
    try:
        lang = state_read(message,"lang");
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        if lang == "ru":
            cursor.execute("SELECT cat_id FROM category WHERE name = '"+str(name)+"'");
        else:
            cursor.execute("SELECT cat_id FROM category WHERE name_uz = '"+str(name)+"'");
        results = cursor.fetchall()
        conn.close()
        return results[0][0]
    except Exception as e:
        logger(message,e)
def basket_add(message,name,price,how_many):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        table = "states"
        #column = str(place)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM basket WHERE name = '"+str(name)+"'")
        results = cursor.fetchall()
        if len(results)==0:
            cursor.execute("INSERT INTO basket VALUES('"+str(name)+"','"+str(price)+"','"+str(how_many)+"')")
        else:
            cursor.execute('''DELETE FROM basket WHERE name = ?''',(name,))
            cursor.execute("INSERT INTO basket VALUES('"+str(name)+"','"+str(price)+"','"+str(how_many)+"')")
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def basket_del(message,name):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM basket WHERE name = ?''',(name,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def basket_del_all(message):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM basket''')
        conn.commit()
        conn.close()
    except Exception as e:
        logger(message,e)
def basket_show(message):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM basket ORDER BY name")
        results = cursor.fetchall()
        conn.close()
        files = []
        for i in range(len(results)):
            files.append(results[i][0])
        return files
    except Exception as e:
        logger(message,e)
def bask_show(message):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM basket ORDER BY name")
        names = cort_to_list(cursor.fetchall())
        bask=[];
        for i in range(len(names)):
            n=stringToArray(names[i].replace(' |','|').replace('| ','|')+"|^")[0];
            cat=n[0];
            prod=n[1];
            print(prod+'<')
            prod_id=db("SELECT id FROM product WHERE name='{0}'".format(prod,))[0];
            cursor.execute("SELECT price FROM basket WHERE name='{0}'".format(names[i],));
            price = cort_to_list(cursor.fetchall())[0]
            cursor.execute("SELECT how_many FROM basket WHERE name='{0}'".format(names[i],));
            how_many = cort_to_list(cursor.fetchall())[0]
            bask.append({"prod_id":prod_id,"name":names[i],"price":price,"how_many":how_many});
        conn.close()
        return bask
    except Exception as e:
        logger(message,e)
def basket_how_many(message,name):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT how_many FROM basket WHERE name = (?)",(name,))
        results = cursor.fetchall()
        conn.close()
        results = results[0][0]
        return results
    except Exception as e:
        logger(message,e)
def basket_price(message,name):
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect("users/"+str(chat_id)+'.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM basket WHERE name = (?)",(name,))
        results = cursor.fetchall()
        conn.close()
        results = results[0][0]
        return results
    except Exception as e:
        logger(message,e)
def product_price(message,name):
    conn = sqlite3.connect('db.sqlite');
    lang = state_read(message,"lang");
    cursor = conn.cursor();
    path = path_read(message);
    try:
        cat = path[len(path)-1];
    except:
        pass
    if lang == "ru":
        try:
            cursor.execute("SELECT id FROM category WHERE name = (?) ",(cat,));
            cat_id = cursor.fetchall()[0][0];
        except:
            cat_id = "0"
        cursor.execute("SELECT price FROM product WHERE name = (?) AND cat_id = (?)",(name,cat_id));
        results = cursor.fetchall();
    else:
        try:
            cursor.execute("SELECT id FROM category WHERE name_uz = (?) ",(cat,));
            cat_id = cursor.fetchall()[0][0];
        except:
            cat_id = "0"
        cursor.execute("SELECT price FROM product WHERE name_uz = (?) AND cat_id = (?)",(name,cat_id));
        results = cursor.fetchall();
    conn.close();
    results = results[0][0];
    return results;
def product_rev(message,name):
    conn = sqlite3.connect('db.sqlite');
    lang = state_read(message,"lang");
    cursor = conn.cursor();
    path = path_read(message);
    try:
        cat = path[len(path)-1];
    except:
        pass
    if lang == "ru":
        try:
            cursor.execute("SELECT id FROM category WHERE name = (?) ",(cat,));
            cat_id = cursor.fetchall()[0][0];
        except:
            cat_id = "0";
        cursor.execute("SELECT rev FROM product WHERE name = (?) AND cat_id = (?)",(name,cat_id));
        results = cursor.fetchall()
    else:
        try:
            cursor.execute("SELECT id FROM category WHERE name_uz = (?) ",(cat,));
            cat_id = cursor.fetchall()[0][0];
        except:
            cat_id = "0";
        cursor.execute("SELECT rev_uz FROM product WHERE name_uz = (?) AND cat_id = (?)",(name,cat_id));
        results = cursor.fetchall()
    conn.close()
    results = results[0][0]
    return results
def product_price_uz(message,name):
    try:
        #chat_id = message.chat.id
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cat = state_read(message,"cat")
        cursor.execute("SELECT id FROM category WHERE name_uz = (?) ",(cat,))
        cat_id = cursor.fetchall()[0][0]

        cursor.execute("SELECT price FROM product WHERE name_uz = (?) AND cat_id = (?)",(name,cat_id))
        results = cursor.fetchall()
        conn.close()
        results = results[0][0]
        return results
    except Exception as e:
        logger(message,e)
def product_rev_uz(message,name):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cat = state_read(message,"cat")
    cursor.execute("SELECT id FROM category WHERE name_uz = (?) ",(cat,))
    cat_id = cursor.fetchall()[0][0]
    cursor.execute("SELECT rev_uz FROM product WHERE name_uz = (?) AND cat_id = (?)",(name,cat_id))
    results = cursor.fetchall()
    conn.close()
    results = results[0][0]
    return results
def db_img_write(data,nameid):
    try:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()
        binary = sqlite3.Binary(data)
        cur.execute("UPDATE product SET img_have = '1' WHERE id = (?)",(nameid,))
        cur.execute("UPDATE product  SET img = (?)  WHERE id = (?)",(binary, nameid))
        con.commit()
        con.rollback()
        con.close()
    except Exception as e:
        logger(message,e)
def db_img_read(message,nameid):
    con = sqlite3.connect('db.sqlite');
    cur = con.cursor();
    lang = state_read(message,"lang");
    path = path_read(message)
    try:
        cat = path[len(path)-1]
    except:
        cat = " "
    if lang == "ru":
        cur.execute("SELECT id FROM category WHERE name = '"+str(cat)+"'")
        cat_id = cur.fetchall()[0][0]
        cur.execute("SELECT img FROM product WHERE name = (?) AND cat_id = (?)",(nameid,cat_id))
        data = cur.fetchone()[0]
    else:
        cur.execute("SELECT id FROM category WHERE name_uz = '"+str(cat)+"'")
        cat_id = cur.fetchall()[0][0]
        cur.execute("SELECT img FROM product WHERE name_uz = (?) AND cat_id = (?)",(nameid,cat_id))
        data = cur.fetchone()[0]  #проччтенное фото
    con.close()
    return data
def db_img_read_uz(message,nameid):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cat = state_read(message,"cat")
    cur.execute("SELECT id FROM category WHERE name_uz = '"+str(cat)+"'")
    cat_id = cur.fetchall()[0][0]
    cur.execute("SELECT img FROM product WHERE name_uz = (?)AND cat_id = (?)",(nameid,cat_id))
    data = cur.fetchone()[0]  #проччтенное фото
    con.close()
    return data
def db_img_cat_read(message,nameid):
    try:
        lang = state_read(message,"lang");
        con = sqlite3.connect('db.sqlite');
        cur = con.cursor();
        if lang == "ru":
            cur.execute("SELECT img FROM category WHERE name = '"+nameid+"'");
        else:
            cur.execute("SELECT img FROM category WHERE name_uz = '"+nameid+"'");
        data = cur.fetchone()[0]  #проччтенное фото
        con.close()
        return data
    except Exception as e:
        logger(message,e)
def db_img_cat_read_uz(message,nameid):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute("SELECT img FROM category WHERE name_uz = '"+nameid+"'")
    data = cur.fetchone()[0]  #проччтенное фото
    con.close()
    return data
def stringToArray(string):
    prods=[];
    prod_mass=[];
    tov=""
    for i in string:
        if i=="^":
            prod_mass.append(prods);
            prods=[];
        elif i =="|":
            prods.append(tov);
            tov="";
        else:
            tov=tov+i;
    return prod_mass;
def db_read(column,table,nameid):
    try:
        try:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT "+str(column)+" FROM "+str(table)+" WHERE name = '"+str(nameid)+"'")
            results = cursor.fetchall()
            conn.close()
            str_files = results[0][0]
            return str_files
        except:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT "+str(column)+" FROM "+str(table)+" WHERE name_uz = '"+str(nameid)+"'")
            results = cursor.fetchall()
            conn.close()
            str_files = results[0][0]
            return str_files
    except Exception as e:
        logger(message,e)
def L(chat_id):
    #lang
    if type(chat_id)==int:
        pass;
    else:
        chat_id=str(message.chat.id);
    print(chat_id)
    try:
        conn = sqlite3.connect('users/{0}.sqlite'.format(str(chat_id)));
        cursor = conn.cursor();
        cursor.execute("SELECT value FROM states WHERE key='lang'");
        lang = cursor.fetchall()[0][0];
        conn.close();
    except:
        conn = sqlite3.connect('users/{0}.sqlite'.format(str(chat_id)));
        cursor = conn.cursor();
        cursor.execute("UPDATE states SET value='{0}' WHERE key='lang'".format(str(chat_id)));
        conn.commit();
        conn.close();
        lang='ru'
    return lang;
def cat_list(message,column):
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        try:
            path = path_read(message)
            try:
                cat = path[len(path)-1]
                cat_id = get_cat_id(message,cat)
            except:
                cat_id = "0";
            cursor.execute("SELECT "+str(column)+" FROM category WHERE work = '1' AND cat_id = '"+str(cat_id)+"'")
            results = cursor.fetchall()
            cursor.execute("SELECT "+str(column)+" FROM product WHERE work = '1' AND cat_id = '"+str(cat_id)+"'")
            results2 = cursor.fetchall()
        except:
            cursor.execute("SELECT "+str(column)+" FROM category WHERE work = '1' AND cat_id = '0'")
            results = cursor.fetchall()
            results2 = []
        conn.close()
        files = []
        for i in range(len(results)):
            files.append(results[i][0])
        for i in range(len(results2)):
            files.append(results2[i][0])
        return files
    except Exception as e:
        logger(message,e)
#+++++++++++++функционал++++++

#++++++++++++++клавиатура
def keyboard_group(message):
    try:
        lang = state_read(message,"lang");
        markup = types.InlineKeyboardMarkup(row_width=3);
        if lang == "ru":
            url_button = types.InlineKeyboardButton(text="Присоединиться к группе", url='https://t.me/+ViWxuPCOsOmRnD3z');
        else:
            url_button = types.InlineKeyboardButton(text="Guruhga qo'shiling", url='https://t.me/+ViWxuPCOsOmRnD3z');
        markup.row(url_button);
        return markup;
    except Exception as e:
        logger(message,e);
def keyboard_district(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True);
        if L(message.chat.id) == "uz":
            btn = types.KeyboardButton("⬅️Orqaga");
        else:
            btn = types.KeyboardButton("⬅️Назад");
        markup.row(btn);
        btn = types.KeyboardButton("Шайхантахур");
        btn1 = types.KeyboardButton("Мирзо-Улугбек");
        markup.row(btn,btn1);
        btn = types.KeyboardButton("Алмазар");
        btn1 = types.KeyboardButton("Юнус-Абад");
        markup.row(btn,btn1);
        btn = types.KeyboardButton("Яккасарай");
        btn1 = types.KeyboardButton("Яшнабад");
        markup.row(btn,btn1);
        btn = types.KeyboardButton("Куйлюк");
        btn1 = types.KeyboardButton("Бектемир");
        markup.row(btn,btn1);
        btn = types.KeyboardButton("Сергели");
        btn1 = types.KeyboardButton("Чиланзар");
        markup.row(btn,btn1);
        btn = types.KeyboardButton("Мирабад");
        btn1 = types.KeyboardButton("Учтепа");
        markup.row(btn,btn1);
        return markup;
    except Exception as e:
        logger(e);
def keyboard_on_cat_podcat(message,files):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True);
        for i in range(len(files)):
            btn = types.KeyboardButton(files[i]);
            markup.row(btn);
        btnback = types.KeyboardButton("⬅️ Назад");
        markup.row(btnback);
        return markup;
    except Exception as e:
        logger(message,e)
def keyboard_admin(message):
    try:
        file=open("prof","r");
        v=file.read();
        file.close();
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True);
        btn1 = types.KeyboardButton("Вернуть всех в начало");
        btn2 = types.KeyboardButton("Профилактика"+v);
        markup.row(btn1,btn2);
        btn1 = types.KeyboardButton("Отправить заказы");
        markup.row(btn1);
        btn1 = types.KeyboardButton("Удалить заказ");
        markup.row(btn1);
        btn1 = types.KeyboardButton("Включить подкатегорию");
        btn2 = types.KeyboardButton("Включить категорию");
        markup.row(btn1,btn2);
        btn1 = types.KeyboardButton("Внести изменения");
        markup.row(btn1);
        btn9 = types.KeyboardButton("Сделать рассылку");
        btn10 = types.KeyboardButton("Изменить дни");
        markup.row(btn9,btn10);
        btn9 = types.KeyboardButton("Сменить пароль");
        btn10 = types.KeyboardButton("Изменить инфо");
        markup.row(btn9,btn10);
        btn9 = types.KeyboardButton("Изменить адрес");
        markup.row(btn9);
        btnback = types.KeyboardButton("⬅️ Назад");
        markup.row(btnback);
        return markup;
    except Exception as e:
        logger(message,e)

def keyboard_location(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btn1 = types.KeyboardButton("📱Joylashuvni yuborish", request_location=True)
            btn2 = types.KeyboardButton("🏃‍♂️Ko'tarish ")
            btnback = types.KeyboardButton("⬅️ Orqaga")
        else:
            btn1 = types.KeyboardButton("📱Отправить локацию", request_location=True)
            btn2 = types.KeyboardButton("🏃‍♂️Самовывоз")
            btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btn1)#,btn2)
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_location_admin(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn1 = types.KeyboardButton("📱Отправить локацию", request_location=True)
        btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btn1)
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_new_or_old(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        btn1 = types.KeyboardButton("Новые")
        btn2 = types.KeyboardButton("Старые")
        markup.row(btn1,btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_new_or_old2(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True);
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        cursor.execute("SELECT name FROM drivers WHERE work = '1'");
        drivers = cursor.fetchall();
        conn.close();
        btnback = types.KeyboardButton("⬅️ Назад");
        markup.row(btnback);
        for driver in drivers:
            btn1 = types.KeyboardButton(driver[0]);
            markup.row(btn1);
        return markup;
    except Exception as e:
        logger(message,e)

def keyboard_back(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btnback = types.KeyboardButton("⬅️ Orqaga")
        else:
            btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_change_days(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT day1 FROM days")
        day1 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day2 FROM days")
        day2 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day3 FROM days")
        day3 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day4 FROM days")
        day4 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day5 FROM days")
        day5 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day6 FROM days")
        day6 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day7 FROM days")
        day7 = cursor.fetchall()[0][0]
        btn = types.KeyboardButton(day1+"Понедельник")
        btn2 = types.KeyboardButton(day2+"Вторник")
        btn3 = types.KeyboardButton(day3+"Среда")
        markup.row(btn,btn2,btn3)
        btn4 = types.KeyboardButton(day4+"Четверг")
        btn5 = types.KeyboardButton(day5+"Пятница")
        btn6 = types.KeyboardButton(day6+"Суббота")
        markup.row(btn4,btn5,btn6)
        btn = types.KeyboardButton(day7+"Воскресенье")
        markup.row(btn)
        #
        z=22;
        for i in range(9):
            cursor.execute("SELECT day{0} FROM days".format(str(z)));
            day = cursor.fetchall()[0][0];
            btn = types.KeyboardButton(day+str(z));
            markup.row(btn);
            z+=1;

        #
        btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        conn.close();
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_day_week(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btnback = types.KeyboardButton("⬅️ Orqaga")
        else:
            btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT day1 FROM days")
        day1 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day2 FROM days")
        day2 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day3 FROM days")
        day3 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day4 FROM days")
        day4 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day5 FROM days")
        day5 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day6 FROM days")
        day6 = cursor.fetchall()[0][0]
        cursor.execute("SELECT day7 FROM days")
        day7 = cursor.fetchall()[0][0]
        if lang == "ru":
            btn1 = types.KeyboardButton("Понедельник")
            if "✅" in day1:
                markup.row(btn1)
            btn2 = types.KeyboardButton("Вторник")
            if "✅" in day2:
                markup.row(btn2)
            btn3 = types.KeyboardButton("Среда")
            if "✅" in day3:
                markup.row(btn3)
            btn4 = types.KeyboardButton("Четверг")
            if "✅" in day4:
                markup.row(btn4)
            btn5 = types.KeyboardButton("Пятница")
            if "✅" in day5:
                markup.row(btn5)
            btn6 = types.KeyboardButton("Суббота")
            if "✅" in day6:
                markup.row(btn6)
            btn7 = types.KeyboardButton("Воскресенье")
            if "✅" in day7:
                markup.row(btn7)
        else:
            btn1 = types.KeyboardButton("Dushanba")
            if "✅" in day1:
                markup.row(btn1)
            btn2 = types.KeyboardButton("Seshanba")
            if "✅" in day2:
                markup.row(btn2)
            btn3 = types.KeyboardButton("Chorshanba")
            if "✅" in day3:
                markup.row(btn3)
            btn4 = types.KeyboardButton("Payshanba")
            if "✅" in day4:
                markup.row(btn4)
            btn5 = types.KeyboardButton("Juma")
            if "✅" in day5:
                markup.row(btn5)
            btn6 = types.KeyboardButton("Shanba")
            if "✅" in day6:
                markup.row(btn6)
            btn7 = types.KeyboardButton("Yakshanba")
            if "✅" in day7:
                markup.row(btn7)
        #
        z=22;
        for i in range(9):
            cursor.execute("SELECT day{0} FROM days".format(str(z)));
            day = cursor.fetchall()[0][0]
            btn = types.KeyboardButton(str(z));
            if "✅" in day:
                markup.row(btn);
            z+=1;

        #
        conn.close();
        return markup;
    except Exception as e:
        logger(message,e)

def keyboard_pay_form(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btnback = types.KeyboardButton("Naqd pul")
            btn1 = types.KeyboardButton("PayMe")
            btn2 = types.KeyboardButton("Click")
        else:
            btnback = types.KeyboardButton("Наличные")
            btn1 = types.KeyboardButton("PayMe")
            btn2 = types.KeyboardButton("Click")
        markup.row(btn1,btn2)
        markup.row(btnback)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_changes(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn1 = types.KeyboardButton("Изменить цену")
        btn2 = types.KeyboardButton("Изменить описание")
        markup.row(btn1,btn2)
        btn1 = types.KeyboardButton("Добавить узб описание")
        btn2 = types.KeyboardButton("Добавить узб имя")
        markup.row(btn1,btn2)
        btn1 = types.KeyboardButton("Добавить фото")
        btn2 = types.KeyboardButton("Удалить продукт")
        markup.row(btn1,btn2)
        btn1 = types.KeyboardButton("Удалить фото")
        btn2 = types.KeyboardButton("Изменить имя продукта")
        markup.row(btn1,btn2)
        btn2 = types.KeyboardButton("⬅️ Назад")
        markup.row(btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_send_loc(message,last_index):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn = types.InlineKeyboardButton(text="Получить локацию", callback_data=str(last_index)+"get_location")
        markup.row(btn)
        btn = types.InlineKeyboardButton(text="Доставлен", callback_data=str(last_index)+"order_done")
        markup.row(btn)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_comment(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btnback = types.KeyboardButton("Без доп. контакта")
        else:
            btnback = types.KeyboardButton("Без доп. контакта")
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_pay_var(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btnback = types.KeyboardButton("⬅️ Orqaga")
        else:
            btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        btn1 = types.KeyboardButton("PayMe")
        btn2 = types.KeyboardButton("Click")
        markup.row(btn1,btn2)
        btn1 = types.KeyboardButton("Наличные")
        markup.row(btn1)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_photo(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn = types.KeyboardButton("Пропустить")
        markup.row(btn)
        btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_menu(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        lang = state_read(message,"lang")
        btnback = types.KeyboardButton("Проверить статус заказа")
        #markup.row(btnback)
        if lang == "uz":
            btnback = types.KeyboardButton("Infoℹ️")
            markup.row(btnback)
            btnback = types.KeyboardButton("Mahsulotlar")
            markup.row(btnback)
            btn1 = types.KeyboardButton("☎️Kontaktlar")
            btn2 = types.KeyboardButton("📥 Savat")
            markup.row(btn1,btn2)
            btnback = types.KeyboardButton("Qo`llab-quvvatlash xizmati📳")
            markup.row(btnback)
        else:
            btnback = types.KeyboardButton("Инфоℹ️")
            markup.row(btnback)
            btnback = types.KeyboardButton("Продукция")
            markup.row(btnback)
            btn1 = types.KeyboardButton("☎️Контакты")
            btn2 = types.KeyboardButton("📥 Корзина")
            markup.row(btn1,btn2)
            btnback = types.KeyboardButton("Служба поддержки📳")
            markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        lang = state_read(message,"lang")

        if key_hard == False:
            if lang == "uz":
                files = cat_list(message,"name_uz")
            if lang == "ru":
                files = cat_list(message,"name")
            iLast = 0
            if lang == "uz":
                btnback = types.KeyboardButton("⬅️ Orqaga")
            else:
                btnback = types.KeyboardButton("⬅️ Назад")
            markup.row(btnback)
            for i in range(len(files)):
                a = i + iLast
                z = a + 1
                iLast = iLast + 1
                conn = sqlite3.connect('db.sqlite')
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM product")
                res1 = cursor.fetchall()
                cursor.execute("SELECT name_uz FROM product")
                res2 = cursor.fetchall()
                names = [];
                for j in range(len(res1)):
                    names.append(res1[j][0])
                    names.append(res2[j][0])
                conn.close()
                try:
                    path = path_read(message);
                    strPath = "";
                    for p in path:
                        strPath+=p;
                    if files[a] in names and "игры" not in strPath and "Bolalar uchun" not in strPath:
                        if lang == "ru":
                            kg = "";
                        else:
                            kg = "";
                    else:
                        kg = "";
                except:
                    kg = "";
                try:
                    btnA = types.KeyboardButton(files[a]+kg)
                    btnZ = types.KeyboardButton(files[z]+kg)
                    markup.row(btnA,btnZ)
                except:
                    try:
                        btnA = types.KeyboardButton(files[a]+kg)
                        markup.row(btnA)
                        break
                    except:
                        btnA = types.KeyboardButton(files[a-1]+kg)
                        #markup.row(btnA)
                        break
            admin_active = state_read(message,"admin_active")
            if admin_active == "0":
                if lang == "uz":
                    btn13 = types.KeyboardButton("📥 Savat")
                    btn14 = types.KeyboardButton("🚖 Tekshirib ko'rmoq")
                else:
                    btn13 = types.KeyboardButton("📥 Корзина")
                    btn14 = types.KeyboardButton("🚖 Оформить заказ")
                markup.row(btn13,btn14)
            else:
                btn13 = types.KeyboardButton("Создать продукт")
                btn14 = types.KeyboardButton("Создать категорию")
                markup.row(btn13,btn14)
                btn1 = types.KeyboardButton("Удалить категорию")
                btn2 = types.KeyboardButton("Удалить фото категории")
                markup.row(btn1,btn2)
                btn13 = types.KeyboardButton("Изменить имя категории")
                btn14 = types.KeyboardButton("Изменить узб имя категории")
                markup.row(btn13,btn14)
            return markup
        else:
            pass
    except Exception as e:
        logger(message,e)

def keyboard_basket(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        lang = state_read(message,"lang")
        if lang == "uz":
            btn10 = types.KeyboardButton("⬅️ Orqaga")
            btn11 = types.KeyboardButton("Aniq")
        else:
            btn10 = types.KeyboardButton("⬅️ Назад")
            btn11 = types.KeyboardButton("Очистить")
        markup.row(btn10,btn11)
        files = basket_show(message)
        for i in range(len(files)):
            file = files[i].replace(".txt","")
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            print(file)
            if "5 лет" in file or "5 yo`sh" in file:
                strFile = file.replace("До 5 лет ","").replace("От 5 лет ","").replace("5 yo`shgacha ","").replace("5 yo`shdan ","")
                print(strFile)
                try:
                    cursor.execute("SELECT cat_id FROM product WHERE name = '"+str(strFile)+"'")
                    cat_id = cursor.fetchall()[0][0];
                except:
                    cursor.execute("SELECT cat_id FROM product WHERE name_uz = '"+str(strFile)+"'")
                    cat_id = cursor.fetchall()[0][0];
            else:
                cat_id=""
            conn.close()
            kg = ""
            if cat_id != "12" and cat_id != "13":
                if lang == "ru":
                    kg = "";
                else:
                    kg = "";
            btn = types.KeyboardButton("❌"+file+kg)
            markup.row(btn)
        if lang == "uz":
            btn12 = types.KeyboardButton("🚖 Tekshirib ko'rmoq")
        else:
            btn12 = types.KeyboardButton("🚖 Оформить заказ")
        markup.row(btn12)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_yes_no(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btn1 = types.KeyboardButton("✅Ha")
            btn2 = types.KeyboardButton("❌Yo'q")
            markup.row(btn1,btn2)
            btnback = types.KeyboardButton("⬅️ Orqaga")
            markup.row(btnback)
        else:
            btn1 = types.KeyboardButton("✅Да")
            btn2 = types.KeyboardButton("❌Нет")
            markup.row(btn1,btn2)
            btnback = types.KeyboardButton("⬅️ Назад")
            markup.row(btnback)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_num(message):
    try:
        path = str(path_read(message))
        bask = message.text;
        print(path)
        if "КРЫЛЬЯ ИНДЕЙКИ" in bask:
            var="кг"
        elif "Буженина" in bask or "Колбаса из курицы" in bask or "Мини колбаски" in bask or "Копченное филе индейки" in bask or "Маленькая" in bask or "Средняя" in bask or "Большая" in bask or "Индейка" in path or "Индоутка" in bask or "Гусь" in bask or "Копченая курица" in bask:
            var = "шт";
        else:
            var = "кг";
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn13 = types.KeyboardButton("⏩")
        #markup.row(btn13)
        #btn1 = types.KeyboardButton("0.5"+var)
        #if "Фарш" in bask and "говяжий" not in bask:
        #    markup.row(btn1)
        btn1 = types.KeyboardButton("1"+var)
        btn2 = types.KeyboardButton("2"+var)
        btn3 = types.KeyboardButton("3"+var)
        if "Печень" in message.text:
            markup.row(btn3)
        else:
            markup.row(btn1,btn2,btn3)
        btn4 = types.KeyboardButton("4"+var)
        btn5 = types.KeyboardButton("5"+var)
        btn6 = types.KeyboardButton("6"+var)
        markup.row(btn4,btn5,btn6)
        btn7 = types.KeyboardButton("7"+var)
        btn8 = types.KeyboardButton("8"+var)
        btn9 = types.KeyboardButton("9"+var)
        markup.row(btn7,btn8,btn9)
        btn11 = types.KeyboardButton("10"+var)
        if lang == "uz":
            btn10 = types.KeyboardButton("📥 Savat")
            btn12 = types.KeyboardButton("⬅️ Orqaga")
        else:
            btn10 = types.KeyboardButton("📥 Корзина")
            btn12 = types.KeyboardButton("⬅️ Назад")

        markup.row(btn10,btn11,btn12)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_num1(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn13 = types.KeyboardButton("⏮")
        markup.row(btn13)
        btn1 = types.KeyboardButton("11")
        btn2 = types.KeyboardButton("12")
        btn3 = types.KeyboardButton("13")
        markup.row(btn1,btn2,btn3)
        btn4 = types.KeyboardButton("14")
        btn5 = types.KeyboardButton("15")
        btn6 = types.KeyboardButton("16")
        markup.row(btn4,btn5,btn6)
        btn7 = types.KeyboardButton("17")
        btn8 = types.KeyboardButton("18")
        btn9 = types.KeyboardButton("19")
        markup.row(btn7,btn8,btn9)
        btn11 = types.KeyboardButton("20")
        if lang == "uz":
            btn10 = types.KeyboardButton("📥 Savat")
            btn12 = types.KeyboardButton("⬅️ Orqaga")
        else:
            btn10 = types.KeyboardButton("📥 Корзина")
            btn12 = types.KeyboardButton("⬅️ Назад")
        markup.row(btn10,btn11,btn12)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_time(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "ru":
            btn = types.KeyboardButton("Без комментария")
            btnback = types.KeyboardButton("⬅️ Назад")
        else:
            btn = types.KeyboardButton("Izohlarsiz ")
            btnback = types.KeyboardButton("⬅️ Orqaga")
        markup.row(btn)
        #markup.row(btnback)
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_ok(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btn1 = types.KeyboardButton("Tasdiqlang")
        else:
            btn1 = types.KeyboardButton("Подтвердить")
        markup.row(btn1)
        if lang == "uz":
            btn2 = types.KeyboardButton("⬅️ Orqaga")
        else:
            btn2 = types.KeyboardButton("⬅️ Назад")
        markup.row(btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_language(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btn1 = types.KeyboardButton("RU🇷🇺")
        btn2 = types.KeyboardButton("UZ🇺🇿")
        markup.row(btn1,btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_contact(message):
    try:
        lang = state_read(message,"lang")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        if lang == "uz":
            btn1 = types.KeyboardButton("📱Kontaktni yuboring", request_contact=True)
            btnback = types.KeyboardButton("⬅️ Orqaga")
        else:
            btn1 = types.KeyboardButton("📱Отправить контакт", request_contact=True)
            btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btn1)
        markup.row(btnback)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_pro_add(message):
    try:
        path = path_read(message)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        var = state_read(message,"check_var")
        btn1 = types.KeyboardButton("⬅️ Orqaga")
        if var == "new_cat" or var == "new_auto":
            btn2 = types.KeyboardButton("Создать здесь")
            markup.row(btn1,btn2)
        elif var == "del_cat":
            btn2 = types.KeyboardButton("Удалить раздел")
            markup.row(btn1,btn2)
        elif var == "new_photo":
            btn2 = types.KeyboardButton("Добавить сюда")
            markup.row(btn1,btn2)
        else:
            markup.row(btn1)
        files = os.listdir("product/"+path)
        try:
            if var == "change_price":
                file = open("product/"+path_read(message)+"price.txt","r")
                file.close()
                state(message,"file_name",str(message.text))
                bot.send_message(message.chat.id, "Введите цену",reply_markup=keyboard_back(message))
                bot_register_next_step_handler(message, "check_new_info");

            if var == "new_photo":
                for i in range(len(files)):
                    if ".jpg" not in files[i] and ".txt" not in files[i]:
                        prod = files[i]
                        btn = types.KeyboardButton(prod)
                        markup.row(btn)
            else:
                for i in range(len(files)):
                    if ".jpg" not in files[i] and ".txt" not in files[i]:
                        prod = files[i]
                        btn = types.KeyboardButton(prod)
                        markup.row(btn)
        except:
            bot.send_message(message.chat.id,"ok")
            if var == "new_cat" or var == "new_auto" or var == "new_photo":
                for i in range(len(files)):
                    if ".jpg" not in files[i] and ".txt" not in files[i]:
                        prod = files[i]
                        btn = types.KeyboardButton(prod)
                        markup.row(btn)

            elif var == "del_cat":
                for i in range(len(files)):
                    if ".jpg" not in files[i] and ".txt" not in files[i]:
                        prod = files[i]
                        btn = types.KeyboardButton(prod)
                        markup.row(btn)
            else:
                for i in range(len(files)):
                    prod = files[i]
                    if ".jpg" not in files[i] and ".txt" not in files[i]:
                        btn = types.KeyboardButton(prod)
                        markup.row(btn)
                    else:
                        if "prod" in files[i]:
                            prod = prod.replace("prod","")
                            prod = prod.replace(".txt","")
                            btn = types.KeyboardButton(prod)
                            markup.row(btn)


        return markup
    except Exception as e:
        logger(message,e)

def keyboard_path(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        btnback = types.KeyboardButton("⬅️ Назад")
        markup.row(btnback)
        btn1 = types.KeyboardButton("Пропустить")
        btn2 = types.KeyboardButton("Выбрать товар")
        markup.row(btn1,btn2)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_post():
    try:
        file = open("post_info/cat","r")
        cat = file.read()
        file.close()
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton(text="Заказать", callback_data="del_this"+str(cat))
        markup.row(btn1)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_inline_days(message):
    try:
        day1=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Понедельник'")));
        day2=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Вторник'")));
        day3=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Среда'")));
        day4=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Четверг'")));
        day5=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Пятница'")));
        day6=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Суббота'")));
        day7=str(len(db("SELECT id FROM orders WHERE status='1' AND day='Воскресенье'")));

        markup = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton(text="Понедельник("+day1+")", callback_data="day1")
        btn2 = types.InlineKeyboardButton(text="Вторник("+day2+")", callback_data="day2")
        btn3 = types.InlineKeyboardButton(text="Среда("+day3+")", callback_data="day3")
        markup.row(btn1,btn2,btn3)
        btn1 = types.InlineKeyboardButton(text="Четверг("+day4+")", callback_data="day4")
        btn2 = types.InlineKeyboardButton(text="Пятница("+day5+")", callback_data="day5")
        btn3 = types.InlineKeyboardButton(text="Суббота("+day6+")", callback_data="day6")
        markup.row(btn1,btn2,btn3)
        btn1 = types.InlineKeyboardButton(text="Воскресенье("+day7+")", callback_data="day7")
        btn2 = types.InlineKeyboardButton(text="Закрыть❌", callback_data="dayClose")
        markup.row(btn1,btn2)
        #
        z=22;
        for i in range(9):
            day=str(len(db("SELECT id FROM orders WHERE day = '{0}' AND status='1'".format(str(z)))));
            btn = types.InlineKeyboardButton(text="{1}({0})".format(day,str(z)), callback_data="day{0}".format(str(z)));
            markup.row(btn);
            z+=1;
        #
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_for_edit(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton(text="Изменить", callback_data="edit_this")
        markup.row(btn1)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_status(message,status,num):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        if status == "1":
            btn1 = types.InlineKeyboardButton(text="Отправить", callback_data="send_status"+str(num))
            markup.row(btn1)
        elif status == "2":
            btn1 = types.InlineKeyboardButton(text="Доставлен", callback_data="get_status"+str(num))
            markup.row(btn1)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_off_driver(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True);
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        cursor.execute("SELECT name FROM drivers WHERE work = '1'");
        results = cursor.fetchall();
        conn.close();
        for i in range(len(results)):
            btnback = types.KeyboardButton(results[i][0]);
            markup.row(btnback);
        btnback = types.KeyboardButton("⬅️ Назад");
        markup.row(btnback);
        return markup;
    except Exception as e:
        logger(message,e)

def keyboard_on_driver(message):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True);
        conn = sqlite3.connect('db.sqlite');
        cursor = conn.cursor();
        cursor.execute("SELECT name FROM drivers WHERE work = '0'");
        results = cursor.fetchall();
        conn.close();
        for i in range(len(results)):
            btnback = types.KeyboardButton(results[i][0]);
            markup.row(btnback);
        btnback = types.KeyboardButton("⬅️ Назад");
        markup.row(btnback);
        return markup;
    except Exception as e:
        logger(message,e)

def keyboard_site(message):
    try:
        lang = state_read(message,"lang");
        markup = types.InlineKeyboardMarkup(row_width=3);
        if lang == "ru":
            url_button = types.InlineKeyboardButton(text="Посетить сайт", url="http://kay-kay.uz/ru");
        else:
            url_button = types.InlineKeyboardButton(text="Saytga tashrif buyuring", url="http://kay-kay.uz/ru");
        markup.row(url_button);
        return markup;
    except Exception as e:
        logger(message,e);

def keyboard_site2(message):
    try:
        lang = state_read(message,"lang");
        markup = types.InlineKeyboardMarkup(row_width=3);
        if lang == "ru":
            url_button = types.InlineKeyboardButton(text="Напишите нам", url="https://t.me/Diana8471");
        else:
            url_button = types.InlineKeyboardButton(text="Bizga yozing", url="https://t.me/Diana8471");
        markup.row(url_button);
        return markup;
    except Exception as e:
        logger(message,e);

def keyboard_send(message,del_id):
    try:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM drivers WHERE work = '1'")
        results = cursor.fetchall()
        conn.close()
        files = [];
        for res in results:
            files.append(res[0]);
        iLast = 0;
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(len(files)):
            a = i + iLast;
            z = a + 1;
            iLast = iLast + 1;
            try:
                btnA = types.InlineKeyboardButton(text="Водитель "+str(files[a]), callback_data=str(del_id)+"_drive"+str(files[a]))
                btnZ = types.InlineKeyboardButton(text="Водитель "+str(files[z]), callback_data=str(del_id)+"_drive"+str(files[z]))
                markup.row(btnA,btnZ)
            except:
                try:
                    btnA = types.InlineKeyboardButton(text="Водитель "+str(files[a]), callback_data=str(del_id)+"_drive"+str(files[a]))
                    markup.row(btnA)
                    break
                except:
                    break
        btn2 = types.InlineKeyboardButton(text="Отклонить❌", callback_data=str(del_id)+"no")
        #markup.row(btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_accept(message,last_index):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton(text="Принять✅", callback_data=str(last_index)+"accept")
        btn2 = types.InlineKeyboardButton(text="Отклонить❌", callback_data=str(last_index)+"no")
        markup.row(btn1,btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_del_loc(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn2 = types.InlineKeyboardButton(text="Удалить локацию❌", callback_data="remove_location")
        markup.row(btn2)
        return markup
    except Exception as e:
        logger(message,e)
def keyboard_cancel_option(message,chat_id):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn2 = types.InlineKeyboardButton(text="Неверно указан номер телефона", callback_data=str(chat_id)+"option1");
        markup.row(btn2)
        btn2 = types.InlineKeyboardButton(text="Не указан узбекский номер телефона", callback_data=str(chat_id)+"option2");
        markup.row(btn2)
        btn2 = types.InlineKeyboardButton(text="Свяжитесь с администратором группы", callback_data=str(chat_id)+"option3");
        markup.row(btn2)

        return markup
    except Exception as e:
        logger(message,e)

def keyboard_resend(last_index):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn2 = types.InlineKeyboardButton(text="✅Доставлен", callback_data=str(last_index)+"done")
        markup.row(btn2)
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_on_podcat(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT cat_id FROM product WHERE work = '0'")
        cat_id = cursor.fetchall()
        for i in range(len(cat_id)):
            cursor.execute("SELECT name FROM category WHERE id = '"+str(cat_id[i][0])+"'")
            cat = cursor.fetchall()[0][0]
            cursor.execute("SELECT name FROM product WHERE work = '0' AND cat_id = '"+str(cat_id[i][0])+"'")
            pod = cursor.fetchall()[0][0]
            cursor.execute("SELECT id FROM product WHERE work = '0' AND cat_id = '"+str(cat_id[i][0])+"'")
            nameid = cursor.fetchall()[0][0]
            if len(str(cat))>60:
                cat = cat[:60]
            btn1 = types.InlineKeyboardButton(text=str(cat)+" "+str(pod), callback_data=str(nameid)+"ID")
            markup.row(btn1)
        conn.close()
        return markup
    except Exception as e:
        logger(message,e)

def keyboard_site_status(message,status,num):
    try:
        markup = types.InlineKeyboardMarkup(row_width=3)
        if status == "Заказ оформлен":
            btn1 = types.InlineKeyboardButton(text="Выехал из магазина", callback_data="1send_site_status"+str(num))
            markup.row(btn1)
        elif status == "Выехал из магазина":
            btn1 = types.InlineKeyboardButton(text="В обработке на складе", callback_data="2send_site_status"+str(num))
            markup.row(btn1)
        elif status == "В обработке на складе":
            btn1 = types.InlineKeyboardButton(text="Вылетел в Ташкент", callback_data="3send_site_status"+str(num))
            markup.row(btn1)
        elif status == "Вылетел в Ташкент":
            btn1 = types.InlineKeyboardButton(text="На растаможке", callback_data="4send_site_status"+str(num))
            markup.row(btn1)
        elif status == "На растаможке":
            btn1 = types.InlineKeyboardButton(text="Готов к доставке", callback_data="5send_site_status"+str(num))
            markup.row(btn1)
        elif status == "Готов к доставке":
            btn1 = types.InlineKeyboardButton(text="Доставлен", callback_data="6send_site_status"+str(num))
            markup.row(btn1)

        return markup
    except Exception as e:
        logger(message,e)
#++++++++++++++клавиатура





bot.polling(none_stop=False)

code=1
