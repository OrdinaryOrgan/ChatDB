USE playstation;

DROP TABLE IF EXISTS achievements;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS games;

CREATE TABLE games
(
    gameid              int primary key not null auto_increment comment 'unique ID of the game',
    title               varchar(100) comment 'name of the game',
    platform            varchar(7) comment 'platform that game published/released',
    developers          varchar(100) comment 'Developers who develop the game',
    publishers          varchar(100) comment 'Publishers who publish/release the game',
    genres              varchar(200) comment 'genre/type of the game',
    supported_languages varchar(400) comment 'languages the game support, can be null if not declared',
    release_date        date comment 'the date that game released'
);

CREATE TABLE achievements
(
    achievementid varchar(20) primary key not null comment 'unique ID of the achievement',
    gameid        int comment 'the id of the game that this achievement belongs to, must be one value in games table',
    title         varchar(200) comment 'name of the achievement',
    description   varchar(2000) comment 'description of the achievement',
    rarity        varchar(8) comment 'rarity/level of the achievement',
    foreign key (gameid) references games (gameid)
);

CREATE TABLE prices
(
    gameid        int primary key not null comment 'unique ID of the game, must be one value in games table',
    usd           decimal(5, 2) comment 'price in US Dollar, use as default currency of price',
    eur           decimal(5, 2) comment 'price in Euro',
    gbp           decimal(5, 2) comment 'price in pound',
    jpy           decimal(6, 1) comment 'price in Japanese Yen',
    rub           decimal(6, 1) comment 'price in rouble',
    date_acquired date comment 'the date that record these information',
    foreign key (gameid) references games (gameid)
);