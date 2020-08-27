library(httr) #Untuk menggunakan fungsi GET
library(ggplot2)

# informasi respon oleh server berupa status, headers, dan body
resp <- GET("https://data.covid19.go.id/public/api/update.json")
# untuk mengetahui status atas permintaan
# 200 = permintaan sukses dipenuhi
resp$status_code #atau status_code(resp)

#Untuk menampilkan metadata yang tersimpan
headers(resp)

#Fungi content untuk mengekstrak konten
cov_id_raw = content(resp, as = "parsed", simplifyVector = TRUE)
length(cov_id_raw) #Jumlah objek
names(cov_id_raw) #Nama objek

#Mengambil objek update dan disimpan ke variabel cov_id_update
cov_id_update <- cov_id_raw$update 
lapply(cov_id_update, names)
cov_id_update$penambahan$tanggal #Tanggal data penambahan
cov_id_update$penambahan$jumlah_sembuh #Penambahan kasus sembuh
cov_id_update$penambahan$jumlah_meninggal #Penambahan kasus meninggal
cov_id_update$total$jumlah_positif #Total kasus positif
cov_id_update$total$jumlah_meninggal #Total kasus meninggal

#Grafik penambahan kasus positif
y <- cov_id_raw$update$harian
y$key_as_string = as.Date(y$key_as_string)
y$jumlah_positif <- lapply(y$jumlah_positif, as.numeric)
ggplot(y, aes(key_as_string, jumlah_positif$value)) +
  geom_line() +
  labs(
    x = NULL,
    y = "Jumlah kasus",
    title = "Grafik Kasus Penambahan COVID-19 Indonesia",
    caption = "Sumber data: covid.19.go.id"
  ) +
  theme_ipsum(
    base_size = 13, 
    plot_title_size = 21,
    grid = "Y",
    ticks = TRUE
  ) +
  theme(plot.title.position = "plot")
