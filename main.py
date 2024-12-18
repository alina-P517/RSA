import random
from tkinter import *
from tkinter.scrolledtext import ScrolledText

class RSA:
    def __init__(self):
        self.p = self.generateNumber()
        self.q = self.generateNumber()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.e(self.phi)
        self.d = self.inverse(self.e, self.phi)

    def generateNumber(self):
        while True:
            num = random.randint(100, 1000)
            if self.prime(num):
                return num

    def prime(self, num):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True

    def e(self, phi):
        e = 3
        while e < phi:
            if self.gcd(e, phi) == 1:
                return e
            e += 2
        return None

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def encrypt(self, plaintext):
        ciphertext = []
        for char in plaintext:
            ciphertext.append(pow(ord(char), self.e, self.n))
        return ciphertext

    def decrypt(self, ciphertext):
        return ''.join(chr(pow(char, self.d, self.n)) for char in ciphertext)


class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root['bg'] = '#cddafa'
        self.root.title('RSA')
        self.root.geometry('1100x600')

        self.rsa = RSA()

        frame = Frame(root, bg='white')
        frame.place(relx=0.05, rely=0.08, width=1000, height=500)

        labelInpt = Label(frame, text='Введите текст:', bg='#cddafa', font=10, anchor="nw")
        labelInpt.grid(row=0, column=0, padx=80, pady=5, sticky='w')

        self.textInpt = ScrolledText(frame, width=100, height=8, relief="solid")
        self.textInpt.grid(row=1, column=0, padx=80, pady=5, sticky='w')

        labelKey = Label(frame, text='Ключ:', bg='#cddafa', font=10, anchor="nw")
        labelKey.grid(row=4, column=0, padx=80, pady=5, sticky='w')

        self.key = Entry(frame, width=133, borderwidth=1, relief="solid")
        self.key.grid(row=6, column=0, padx=80, pady=5, sticky="w")
        self.key.insert(0, f"e: {self.rsa.e}, n: {self.rsa.n}")
        self.key.config(state=DISABLED)

        labelOutpt = Label(frame, text='Результат:', bg='#cddafa', font=10, anchor="nw")
        labelOutpt.grid(row=7, column=0, padx=80, pady=5, sticky='w')

        self.textOutpt = ScrolledText(frame, width=100, height=8, relief="solid")
        self.textOutpt.grid(row=8, column=0, padx=80, pady=5, sticky='w')
        self.textOutpt.config(state=DISABLED)

        btnEncrypt = Button(frame, text='Зашифровать', bg='#cddafa', command=self.encrypt)
        btnEncrypt.grid(row=10, column=0, sticky="w", padx=80, pady=10)

        btnDecrypt = Button(frame, text='Расшифровать', bg='#cddafa', command=self.decrypt)
        btnDecrypt.grid(row=10, column=0, sticky="w", padx=180, pady=10)

    def encrypt(self):
        plaintext = self.textInpt.get("1.0", END).strip()
        if plaintext:
            ciphertext = self.rsa.encrypt(plaintext)
            self.textOutpt.config(state=NORMAL)
            self.textOutpt.delete("1.0", END)
            self.textOutpt.insert(END, ', '.join(map(str, ciphertext)))
            self.textOutpt.config(state=DISABLED)

    def decrypt(self):
        ciphertext = self.textOutpt.get("1.0", END).strip()
        if ciphertext:
            try:
                ciphertext = list(map(int, ciphertext.split(', ')))
                decrypted_text = self.rsa.decrypt(ciphertext)
                self.textOutpt.config(state=NORMAL)
                self.textOutpt.delete("1.0", END)
                self.textOutpt.insert(END, decrypted_text)
                self.textOutpt.config(state=DISABLED)
            except ValueError:
                self.textOutpt.config(state=NORMAL)
                self.textOutpt.delete("1.0", END)
                self.textOutpt.insert(END, "Ошибка: Неверный формат шифротекста.")
                self.textOutpt.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    app = RSAApp(root)
    root.mainloop()
