import qrcode

url = "https://github.com/lippergreem2-cmyk/Nitron"

img = qrcode.make(url)
img.save("Nitron_QR.png")

print("Created: Nitron_QR.png")
