# Güvenli Haberleşme Projesi

## Grup Üyeleri ve Görev Dağılımı

| Ad Soyad | Öğrenci No | Rol | Sorumluluk |
|---|---|---|---|
| Hazal Karayiğit | `448887` | Master (sunucu) |
| Ali Berk Bacaksız | `449460` | İstemci | 
| Alpar Amirahmadov | `445844` | İstemci |

Ortak: Giriş, karşılaşılan sorunlar, sonuç, görev dağılımı tablosu ve commit özeti.

## Dil ve Platform

- Dil: Python 3
- Platform: Masaüstü, TCP socket
- Kütüphaneler: `cryptography`, `kyber-py`

## Mimari

```
İstemci 1 ◄──► Sunucu ◄──► İstemci 2
```

| Bilgisayar | Çalışan program |
|---|---|
| Bilgisayar 1 (Hazal) | `server.py` |
| Bilgisayar 2 | `client.py` (İstemci 1) |
| Bilgisayar 3 | `client.py` (İstemci 2) |


## Durum

- [x] Güvensiz mod (metin + PDF, sunucu üzerinden yönlendirme)
- [ ] Anahtar dağıtım yöntemleri (RSA, DH, ECC, Kyber)
- [ ] Güvenli mod (AES, K1/K2 yeniden şifreleme)
- [ ] Kütüphanesiz AES ve karşılaştırma
- [ ] Süre ve paket boyutu ölçüm tablosu
- [ ] Wireshark yakalamaları (her mod için)
- [ ] Rapor
