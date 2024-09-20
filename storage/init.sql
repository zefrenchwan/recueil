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
    name text unique not null
);

create table entities.inheritances (
    child_id int not null references entities.tags(tag_id), 
    parent_id int references entities.tags(tag_id)
);

create table entities.tokens (
    token_id serial primary key, 
    token_content text not null unique
);

create table entities.homonyms (
    homonym_id serial primary key,
    token_id int not null references entities.tokens(token_id), 
    attributes text not null
);

create table entities.links (
    token_id int not null references entities.tokens(token_id),
    tag_id int not null references entities.tags(tag_id)
);

create procedure entities.insert_value(p_name text, p_description text, p_tag text) language plpgsql as $$
declare
    l_token_id int;
    l_tag_id int;
begin 
    -- insert tag if not found, search is case insensitive
    select T.tag_id into l_tag_id from entities.tags T where T.name ilike p_tag;
    if l_tag_id is null then 
        insert into entities.tags(name) values (p_tag) returning tag_id into l_tag_id;
    end if;

    if not exists (
        select 1
        from entities.homonyms HOM
        join entities.tokens TOK on TOK.token_id = HOM.token_id
        where HOM.attributes = p_description
        and TOK.token_content ilike p_name
    ) then 
        insert into entities.tokens(token_content) values (p_name) returning token_id into l_token_id;
        insert into entities.homonyms(token_id, attributes) values (l_token_id, p_description); 
    end if;
end; $$;

create function entities.load_entity(p_value text)
returns table(token_content text, attributes text, tag text, parents text[]) language plpgsql as $$
declare 
begin 
    -- to complete later 
    return query 
        select 
        null::text as token_content, 
        null::text as attributes, 
        null as tag, 
        array[]::text[] as parents  
        where 1 != 1;
end;$$;