create schema auths;

create table auths.users (
    user_id serial primary key, 
    login text not null unique, 
    active bool not null default true,
    hash_pwd text not null
);

create schema entities;

create table entities.tags (
    tag_id serial primary key,
    name text unique not null, 
    description text
);

create table entities.inheritances (
    child_id int not null references entities.tags(tag_id), 
    parent_id int references entities.tags(tag_id)
);

create or replace view entities.inheritance_tree as 
select CH.child_id, CHTAGS.name as child_name, CH.parent_id, PTAGS.name as parent_name  
from entities.inheritances CH 
join entities.tags CHTAGS on CHTAGS.tag_id = CH.child_id
left join entities.tags PTAGS on CHTAGS.tag_id = CH.parent_id;

