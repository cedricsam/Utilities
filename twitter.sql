--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: tweets; Type: TABLE; Schema: public; Owner: lp; Tablespace: 
--

CREATE TABLE tweets (
    id bigint NOT NULL,
    created_at timestamp with time zone,
    text text,
    in_reply_to_user_id bigint,
    in_reply_to_screen_name character varying(25),
    in_reply_to_status_id bigint,
    screen_name character varying(25),
    source character varying(256),
    user_id bigint,
    retweet_count integer,
    retweeted_status bigint,
    geo geometry,
    CONSTRAINT enforce_dims_geo CHECK ((st_ndims(geo) = 2)),
    CONSTRAINT enforce_geotype_geo CHECK (((geometrytype(geo) = 'POINT'::text) OR (geo IS NULL))),
    CONSTRAINT enforce_srid_geo CHECK ((st_srid(geo) = 4326))
);


ALTER TABLE public.tweets OWNER TO lp;

--
-- Name: twitter_users; Type: TABLE; Schema: public; Owner: lp; Tablespace: 
--

CREATE TABLE twitter_users (
    id bigint NOT NULL,
    retrieved timestamp without time zone,
    name character varying(32),
    screen_name character varying(32) NOT NULL,
    description character varying(512),
    profile_image_url character varying(256),
    url character varying(256),
    protected boolean,
    followers_count integer,
    friends_count integer,
    created_at timestamp without time zone,
    favourites_count integer,
    utc_offset integer,
    time_zone character varying(128),
    profile_background_image_url character varying(256),
    profile_use_background_image boolean,
    notifications boolean,
    geo_enabled boolean,
    verified boolean,
    following integer,
    statuses_count integer,
    lang character varying(8),
    contributors_enabled boolean,
    follow_request_sent boolean,
    listed_count integer,
    show_all_inline_media boolean
);


ALTER TABLE public.twitter_users OWNER TO lp;

--
-- Name: twitter_users_id_seq; Type: SEQUENCE; Schema: public; Owner: lp
--

CREATE SEQUENCE twitter_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.twitter_users_id_seq OWNER TO lp;

--
-- Name: twitter_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: lp
--

ALTER SEQUENCE twitter_users_id_seq OWNED BY twitter_users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: lp
--

ALTER TABLE ONLY twitter_users ALTER COLUMN id SET DEFAULT nextval('twitter_users_id_seq'::regclass);


--
-- Name: tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: lp; Tablespace: 
--

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (id);


--
-- Name: twitter_users_pkey; Type: CONSTRAINT; Schema: public; Owner: lp; Tablespace: 
--

ALTER TABLE ONLY twitter_users
    ADD CONSTRAINT twitter_users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

