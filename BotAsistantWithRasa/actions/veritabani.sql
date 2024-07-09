CREATE TABLE IF NOT EXISTS Alisveris 
(
    id INTEGER PRIMARY KEY,
    Urun TEXT NOT NULL,
    Kirmizi INTEGER DEFAULT 0,
    Mavi INTEGER DEFAULT 0,
    Yesil INTEGER DEFAULT 0,
    Sari INTEGER DEFAULT 0
);

INSERT INTO Alisveris (Urun, Kirmizi, Mavi, Yesil, Sari) VALUES ('T-Shirt', 10, 5, 3, 7);
INSERT INTO Alisveris (Urun, Kirmizi, Mavi, Yesil, Sari) VALUES ('Pantolon', 4, 8, 6, 2);
INSERT INTO Alisveris (Urun, Kirmizi, Mavi, Yesil, Sari) VALUES ('Ceket', 6, 3, 5, 1);
INSERT INTO Alisveris (Urun, Kirmizi, Mavi, Yesil, Sari) VALUES ('Elbise', 7, 9, 2, 4);
INSERT INTO Alisveris (Urun, Kirmizi, Mavi, Yesil, Sari) VALUES ('Gömlek', 2, 6, 8, 3);

