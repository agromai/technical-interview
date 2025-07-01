from PIL import Image
import matplotlib.pyplot as plt

arquivos = [
    'daily_sales_trends.png',
    'sales_by_category.png',
    'quantity_vs_price.png'
]

fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for ax, arquivo in zip(axs, arquivos):
    img = Image.open(arquivo)
    ax.imshow(img)
    ax.axis('off')
    ax.set_title(arquivo)

plt.tight_layout()
plt.show()
