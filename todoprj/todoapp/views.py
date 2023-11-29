from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import todo
import string
import math
import numpy as np
import random
# Create your views here.

spasi = "_"
akhirHill = "@"
akhirSpiral = "ദ"


# @login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        task = substitusi_encrypt(spiral_encrypt(task)) 
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    # all_todos = todo.objects.filter(user=request.user)
    all_todos = todo.objects.all()
    decrypt_todos = []
    for todo_item in all_todos:
        decrypt_todo = {
            'id': todo_item.id,
            'todo_name': spiral_decrypt(substitusi_decrypt(todo_item.todo_name)),
            'status': todo_item.status,
        }
        decrypt_todos.append(decrypt_todo)

    context = {
        'decrypt': decrypt_todos
    }
    return render(request, 'todoapp/index.html', context)

# @login_required
def DeleteTask(request, id):
    get_todo = todo.objects.get(id=id, user=request.user)
    get_todo.delete()
    return redirect('home-page')

# @login_required
def Status(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

def Edit(request, id):
    if request.method == 'POST':
        task = request.POST.get('task')
        task = substitusi_encrypt(spiral_encrypt(task)) 
        get_todo = todo.objects.get(user=request.user, id=id)
        get_todo.todo_name = task 
        get_todo.save() 
        return redirect("home-page")
    
    # data = todo.objects.get(user=request.user, id=id)
    data = todo.objects.filter(user=request.user, id=id)
    context = {
        'data': data
    }
    return render(request, 'todoapp/edit.html',context)



# Encryption
def spiral_encrypt(plain_text):  # Fungsi untuk enkripsi
    square_root = math.sqrt(len(plain_text)) # Menghitung akar kuadrat dari panjang plain text

    rounded_step_size = math.ceil(square_root) # Pembulatan ke atas akar kuadrat untuk mendapatkan ukuran langkah yang dibutuhkan

    step_size = rounded_step_size # Menggunakan ukuran langkah yang dibulatkan sebagai ukuran matriks yang akan digunakan

    matrix_representation = (
        []
    )  # Matriks kosong untuk menyimpan representasi matriks dari teks
    encrypted_text = ""  # Teks terenkripsi
    # print("Panjang Matrix nya (m x m) : ", step_size)

    for i in range(step_size):  # Mengisi matriks dengan karakter dari teks
        matrix_row = []  # Baris matriks
        # Loop ini akan mengulangi sebanyak kolom yang diperlukan dalam matriks, dan jumlah kolom dihitung dengan
        # membagi panjang teks (len(plain_text)) dengan step_size, dan menggunakan math.ceil()
        # untuk memastikan hasil pembagian dibulatkan ke atas agar semua karakter teks dapat masuk.
        for j in range(step_size):
            index = (
                j * step_size
                + i  # j = indeks kolom saat ini, step_size = jumlah baris, i = indeks baris saat ini
            )  # Indeks karakter yang akan dimasukkan ke dalam baris matriks
            if index < len(
                plain_text
            ):  # Jika masih ada karakter yang tersisa, masukkan karakter ke dalam baris matriks
                matrix_row.append(
                    plain_text[index]
                )  # Masukkan karakter ke dalam baris matriks
            else:  # Jika tidak ada karakter yang tersisa, masukkan karakter '@' ke dalam baris matriks
                matrix_row.append(akhirSpiral)  # Masukkan karakter '@' ke dalam baris matriks
        matrix_representation.append(
            matrix_row
        )  # Masukkan baris matriks ke dalam matriks representasi
    

    # proses enkripsi
    matrix_height = step_size  # Tinggi matriks
    matrix_width = step_size # Lebar matriks
    mid = step_size // 2 # Nilai Tengah matriks
    x1=0 # Inisiasi banyaknya step/isi matrix


    for i in range(mid): # Looping sebanyak setengah matriks
        if step_size % 2 == 0: # Perulangan ketika `step_size`/panjang matriks genap
            for x in range(mid + i , mid - i -1 , -1): # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak keatas dengan mid + i sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke atas dalam matriks.
                encrypted_text += matrix_representation[x][mid+i] # bergerak keatas sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah (barisnya) dengan iterasi -1 sehingga bergerak keatas
                x1+=1
                # print(x1,matrix_representation[x][mid+i],"(",x,",",mid+i,")")
            for y in range(mid + i , mid - i -1, -1 ): # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekiri dengan mid + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke kiri dalam matriks.
                encrypted_text += matrix_representation[mid-i-1][y] # bergerak kekiri sehingga x nya tidak berubah(barisnya), tetapi y nya berubah (kolomnya) dengan iterasi -1 sehingga bergerak kekiri
                x1+=1
                # print(x1,matrix_representation[mid-i-1][y],"(",mid-i-1,",",y,")")
            for x in range(mid - i - 1, mid + i + 1):  # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kebawah dengan mid -i -1 sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                encrypted_text += matrix_representation[x][mid-i-1] # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                x1+=1
                # print(x1,matrix_representation[x][mid-i-1],"(",x,",",mid-i-1,")")
            if(i+1!=mid): # untuk memeriksa apakah iterasi saat ini bukan iterasi terakhir dalam proses enkripsi(mengecek apakah sudah membentuk full spiral atau belum)
                for y in range(mid - i -1, mid + i + 1, +1): # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekanan dengan mid - i - 1 sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                    encrypted_text += matrix_representation[mid+i+1][y] # bergerak kekanan sehingga x nya tidak berubah(barisnya), tetapi y nya berubah(kolomnya)
                    x1+=1
                    # print(x1,matrix_representation[mid+i+1][y],"(",mid+i+1,",",y,")")
        else: # Perulangan ketika `step_size`/panjang matriks ganjil
            for x in range(mid - i, mid + i + 1): # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kebawah dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                encrypted_text += matrix_representation[x][mid-i] # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                x1+=1
                # print(x1,matrix_representation[x][mid-i],"(",x,",",mid-i,")")
            for y in range(mid - i , mid + i + 1, +1): # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekanan dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                encrypted_text += matrix_representation[mid+i+1][y] # bergerak kekanan sehingga x nya tidak berubah(barisnya), tetapi y nya berubah(kolomnya)
                x1+=1
                # print(x1,matrix_representation[mid+i+1][y],"(",mid+i+1,",",y,")")
            for x in range(mid + i + 1, mid - i -1, -1):  # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak keatas dengan mid + i + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke atas dalam matriks.
                encrypted_text += matrix_representation[x][mid+i+1] # bergerak keatas sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah (barisnya) dengan iterasi -1 sehingga bergerak keatas
                x1+=1
                # print(x1,matrix_representation[x][mid+i+1],"(",x,",",mid+i+1,")")
            for y in range(mid + i +1, mid - i -1, -1 ):  # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekiri dengan mid + i + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke kiri dalam matriks.
                encrypted_text += matrix_representation[mid-i-1][y]  # bergerak kekiri sehingga x nya tidak berubah(barisnya), tetapi y nya berubah (kolomnya) dengan iterasi -1 sehingga bergerak kekiri
                x1+=1
                # print(x1,matrix_representation[mid-i-1][y],"(",mid-i-1,",",y,")")
            if(i+1==mid):
                i+=1
                for x in range(mid - i , mid + i + 1):
                  encrypted_text += matrix_representation[x][mid-i]
                  x1+=1
                #   print(x1,matrix_representation[x][mid-i],"(",x,",",mid-i,")")

    return encrypted_text

def substitusi_encrypt(plaintext):

    # Menghasilkan angka acak antara 1 dan 10
    key = int(random.randint(1,9))
    # list yang berisikan semua 256 karakter
    all_letters= string.ascii_letters #256
        
    dict1 = {}

	# penjumlahan ascii karakter dengan key
    for i in range(len(all_letters)):
        dict1[all_letters[i]] = all_letters[(i+key)%len(all_letters)]

    # variable hasil cipher text
    cipher_txt=[]

    # pengulangan untuk pengecekan karakter
    for char in plaintext:
        if char in all_letters:
            temp = dict1[char]
            cipher_txt.append(temp)
        else:
            temp =char
            cipher_txt.append(temp)
            
    cipher_txt= "".join(cipher_txt)
    middle_index = len(cipher_txt) // 2
    cipher_txt = cipher_txt[:middle_index] + str(key) + cipher_txt[middle_index:]
	# pengembalian hasil cipher text
    return cipher_txt


def substitusi_decrypt(msg):
    # key = int(input("masukkan kunci(angka) : "))
    if len(msg) % 2 == 0:
        key = int(msg[len(msg) // 2 - 1])
        middle_index = len(msg) // 2
        msg = msg[:middle_index - 1] + msg[middle_index:]
        # middle_right_character_even = my_string_even[len(my_string_even) // 2]
    else:
        key = int(msg[len(msg) // 2])
        middle_index = len(msg) // 2
        msg = msg[:middle_index - 1] + msg[middle_index:]
   
    all_letters= string.ascii_letters
    
    dict2 = {}	
    
	# pengurangan ascii karakter dengan kunci
    for i in range(len(all_letters)):
        dict2[all_letters[i]] = all_letters[(i-key)%(len(all_letters))]
        
    # loop to recover plain text
    decrypt_txt = []

	# pengulangan untuk mengembalikan plain text
	# mengecek apakah char ada di msg
    for char in msg:
        # mengecek apakah char ada di all_letter ascii
        if char in all_letters:
            temp = dict2[char]
            decrypt_txt.append(temp)
        else:
            temp = char
            decrypt_txt.append(temp)
            
    decrypt_txt = "".join(decrypt_txt)
    
	# mengembalikan Hasil decrypt 
    return decrypt_txt

# Decryption
def spiral_decrypt(cipher_text):  # Fungsi untuk dekripsi
    # cipher_text = input("Masukkan Cipher text : ")

    square_root = math.sqrt(len(cipher_text)) # Menghitung akar kuadrat dari panjang cipher text

    rounded_step_size = math.ceil(square_root) # Pembulatan ke atas akar kuadrat untuk mendapatkan ukuran langkah yang dibutuhkan

    step_size = rounded_step_size # Menggunakan ukuran langkah yang dibulatkan sebagai ukuran matriks yang akan digunakan

    matrix_height = step_size  # Tinggi matriks
    matrix_width = step_size # Lebar matriks
    mid = step_size // 2 # nilai tengah matriks
    x1=0 # Inisiasi banyaknya step/isi matrix
    plain_text_matrix = (
        [  # Matriks kosong untuk menyimpan representasi matriks dari teks
            [" " for _ in range(matrix_width)] for _ in range(matrix_height)
        ]
    )

    idx = 0  # Indeks untuk mengakses karakter dalam teks terenkripsi

    for i in range(mid):  # Mulai dari tengah
        if matrix_height % 2 == 0:  # Jika tinggi matriks genap
            for x in range(mid + i , mid - i -1 , -1):
                plain_text_matrix[x][mid+i] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[x][mid+i],"(",x,",",mid+i,")")
            for y in range(mid + i , mid - i -1, -1 ):
                plain_text_matrix[mid-i-1][y] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[mid-i-1][y],"(",mid-i-1,",",y,")")
            for x in range(mid - i - 1, mid + i + 1):
                plain_text_matrix[x][mid-i-1] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[x][mid-i-1],"(",x,",",mid-i-1,")")
            if(i+1!=mid):
                for y in range(mid - i -1, mid + i + 1, +1):
                    plain_text_matrix[mid+i+1][y] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks
                    x1+=1
                    # print(x1,plain_text_matrix[mid+i+1][y],"(",mid+i+1,",",y,")")
        else:
            for x in range(mid - i, mid + i + 1):
                plain_text_matrix[x][mid-i] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[x][mid-i],"(",x,",",mid-i,")")
            for y in range(mid - i , mid + i + 1, +1):
                plain_text_matrix[mid+i+1][y] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[mid+i+1][y],"(",mid+i+1,",",y,")")
            for x in range(mid + i + 1, mid - i -1, -1):
                plain_text_matrix[x][mid+i+1] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[x][mid+i+1],"(",x,",",mid+i+1,")")
            for y in range(mid + i +1, mid - i -1, -1 ):
                plain_text_matrix[mid-i-1][y] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1+=1
                # print(x1,plain_text_matrix[mid-i-1][y],"(",mid-i-1,",",y,")")
            if(i+1==mid):
                i+=1
                for x in range(mid - i , mid + i + 1):
                  plain_text_matrix[x][mid-i] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                  idx += 1  # Tambahkan indeks
                  x1+=1
                #   print(x1,plain_text_matrix[x][mid-i],"(",x,",",mid-i,")")


    plain_text = ""  # Teks terdekripsi
    for j in range(matrix_width):  # Untuk setiap kolom dalam matriks representasi
        for i in range(matrix_height):  # Untuk setiap baris dalam matriks representasi
            if plain_text_matrix[i][j] != akhirSpiral:  # Jika bukan karakter akhirSpiral
                plain_text += plain_text_matrix[i][
                    j
                ]  # Tambahkan karakter ke dalam teks terdekripsi
    # print(plain_text)
    return plain_text # Kembalikan - menjadi spasi