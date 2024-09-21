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
    homonym_id int not null references entities.homonyms(homonym_id),
    tag_id int not null references entities.tags(tag_id)
);

create procedure entities.insert_value(p_name text, p_description text, p_tag text) language plpgsql as $$
declare
    l_token_id int;
    l_homonym_id int;
    l_tag_id int;
begin 
    -- insert tag if not found, search is case insensitive
    select T.tag_id into l_tag_id from entities.tags T where T.name ilike p_tag;
    if l_tag_id is null then 
        insert into entities.tags(name) values (p_tag) returning tag_id into l_tag_id;
    end if;

    select token_id into l_token_id from entities.tokens where token_content like p_name;
    if l_token_id is null then 
        insert into entities.tokens(token_content) values (p_name) returning token_id into l_token_id;
    end if;

    if not exists (
        select 1
        from entities.homonyms HOM
        join entities.tokens TOK on TOK.token_id = HOM.token_id
        where HOM.attributes like p_description
        and TOK.token_content ilike p_name
    ) then 
        insert into entities.homonyms(token_id, attributes) values (l_token_id, p_description) returning homonym_id into l_homonym_id; 
        insert into entities.links(homonym_id, tag_id) values (l_homonym_id, l_tag_id);
    end if;
end; $$;


create function entities.load_entity(p_value text)
returns table(token_content text, attributes text, tags text[]) language plpgsql as $$
declare 
    l_walk_id text;
    l_size_before bigint;
    l_size_after bigint;
begin 

    -- create temp table if necessary to deal with the 
    create temporary table if not exists temp_walks(walk_id text, homonym_id int, tag_id int);
    -- insert first level data  
    select gen_random_uuid ()::text into l_walk_id;
    insert into temp_walks(walk_id, homonym_id, tag_id)
    select l_walk_id, HOM.homonym_id, LIN.tag_id
    from entities.homonyms HOM
    join entities.tokens TOK on TOK.token_id = HOM.token_id
    join entities.links LIN on LIN.homonym_id = HOM.homonym_id
    where TOK.token_content ilike p_value;

    
    -- then, walkthrough
    loop 
        select count(*) into l_size_before from temp_walks where walk_id = l_walk_id;

        insert into temp_walks(walk_id, homonym_id, tag_id) 
        select l_walk_id, TWA.homonym_id, INH.parent_id 
        from entities.inheritances INH 
        join temp_walks TWA on TWA.tag_id = INH.child_id 
        where TWA.walk_id = l_walk_id 
        and not exists (
            select 1 
            from entities.inheritances INN_INH
            where TWA.tag_id = INN_INH.parent_id
            and INH.child_id = INN_INH.child_id
        );

        select count(*) into l_size_after from temp_walks where walk_id = l_walk_id;
        exit when l_size_after <= l_size_before;
    end loop;
    
    -- to complete later 
    return query 
        with all_matches as (
            select TOK.token_content, HOM.attributes, TAG.name
            from temp_walks TWA
            join entities.homonyms HOM on HOM.homonym_id = TWA.homonym_id
            join entities.tokens TOK on TOK.token_id = HOM.token_id
            join entities.tags TAG on TAG.tag_id = TWA.tag_id 
            where TWA.walk_id = l_walk_id
        )
        select AMA.token_content, AMA.attributes, array_agg(AMA.name) as tags 
        from all_matches AMA
        group by AMA.token_content, AMA.attributes; 

    delete from temp_walks where walk_id = l_walk_id;
    return; 
end;$$;


create procedure entities.insert_link(p_child text, p_parent text) language plpgsql as $$
declare 
    l_child_id int;
    l_parent_id int;
begin 
    select tag_id into l_child_id from entities.tags where name ilike p_child;
    select tag_id into l_parent_id from entities.tags where name ilike p_parent;
    if l_child_id is null then 
        insert into entities.tags(name) values (p_child) returning tag_id into l_child_id;
    end if; 

    if l_parent_id is null then 
        insert into entities.tags(name) values (p_parent) returning tag_id into l_parent_id;
    end if;

    if not exists (
        select 1 from  entities.inheritances 
        where child_id = l_child_id and parent_id = l_parent_id
    ) then 
        insert into entities.inheritances(child_id, parent_id) values (l_child_id, l_parent_id);
    end if;
end; $$;