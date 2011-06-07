drop table if exists articles;
create table articles (
    id integer primary key autoincrement,
    rank integer not null,
    title string not null,
    link string not null,
    link_origin string not null,
    description text not null,
    points integer not null,
    author string not null,
    author_url string not null,
    comments_count integer not null,
    last_comment text not null,
    last_comment_author string not null,
    last_comment_author_url string not null
);
