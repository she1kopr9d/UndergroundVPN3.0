--
-- PostgreSQL database dump
--

\restrict zQVVgixVcq6LQfUWgZpCYChEWCIXrR4JlwJAJSNKmhpr6SzAorqZzr86oMWRlUr

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg130+1)
-- Dumped by pg_dump version 15.14 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: paymentmethod; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.paymentmethod AS ENUM (
    'crypto',
    'telegram_star',
    'handle',
    'system'
);


ALTER TYPE public.paymentmethod OWNER TO "user";

--
-- Name: paymentmode; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.paymentmode AS ENUM (
    'test',
    'production'
);


ALTER TYPE public.paymentmode OWNER TO "user";

--
-- Name: paymentstatus; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.paymentstatus AS ENUM (
    'pending',
    'moderation',
    'completed',
    'failed'
);


ALTER TYPE public.paymentstatus OWNER TO "user";

--
-- Name: producttype; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.producttype AS ENUM (
    'one_time',
    'recurring'
);


ALTER TYPE public.producttype OWNER TO "user";

--
-- Name: subscriptionstatus; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.subscriptionstatus AS ENUM (
    'active',
    'expired',
    'canceled'
);


ALTER TYPE public.subscriptionstatus OWNER TO "user";

--
-- Name: transactiontype; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.transactiontype AS ENUM (
    'deposit',
    'withdrawal'
);


ALTER TYPE public.transactiontype OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "user";

--
-- Name: configs; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.configs (
    name character varying,
    uuid character varying,
    config character varying,
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    server_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.configs OWNER TO "user";

--
-- Name: configs_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.configs_id_seq OWNER TO "user";

--
-- Name: configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.configs_id_seq OWNED BY public.configs.id;


--
-- Name: finance_accounts; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.finance_accounts (
    id integer NOT NULL,
    balance double precision NOT NULL,
    referral_percent integer NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.finance_accounts OWNER TO "user";

--
-- Name: finance_accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.finance_accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.finance_accounts_id_seq OWNER TO "user";

--
-- Name: finance_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.finance_accounts_id_seq OWNED BY public.finance_accounts.id;


--
-- Name: moderators; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.moderators (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.moderators OWNER TO "user";

--
-- Name: moderators_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.moderators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.moderators_id_seq OWNER TO "user";

--
-- Name: moderators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.moderators_id_seq OWNED BY public.moderators.id;


--
-- Name: payment_receipts; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.payment_receipts (
    id integer NOT NULL,
    file_path character varying NOT NULL,
    filename character varying NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    payment_id integer NOT NULL
);


ALTER TABLE public.payment_receipts OWNER TO "user";

--
-- Name: payment_receipts_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.payment_receipts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_receipts_id_seq OWNER TO "user";

--
-- Name: payment_receipts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.payment_receipts_id_seq OWNED BY public.payment_receipts.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    amount double precision NOT NULL,
    transaction_type public.transactiontype NOT NULL,
    status public.paymentstatus NOT NULL,
    mode public.paymentmode NOT NULL,
    payment_method public.paymentmethod NOT NULL,
    external_id character varying,
    note text,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    finance_account_id integer NOT NULL
);


ALTER TABLE public.payments OWNER TO "user";

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payments_id_seq OWNER TO "user";

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.products (
    price numeric(10,2) NOT NULL,
    product_type public.producttype NOT NULL,
    id integer NOT NULL,
    name character varying,
    duration_days integer,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE public.products OWNER TO "user";

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO "user";

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: server_configs; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.server_configs (
    id integer NOT NULL,
    public_key character varying NOT NULL,
    private_key character varying NOT NULL,
    config_data json NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    server_id integer
);


ALTER TABLE public.server_configs OWNER TO "user";

--
-- Name: server_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.server_configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.server_configs_id_seq OWNER TO "user";

--
-- Name: server_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.server_configs_id_seq OWNED BY public.server_configs.id;


--
-- Name: servers; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.servers (
    name character varying,
    code character varying,
    id integer NOT NULL
);


ALTER TABLE public.servers OWNER TO "user";

--
-- Name: servers_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.servers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.servers_id_seq OWNER TO "user";

--
-- Name: servers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.servers_id_seq OWNED BY public.servers.id;


--
-- Name: subscription_charges; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.subscription_charges (
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    subscription_id integer NOT NULL,
    payment_id integer NOT NULL
);


ALTER TABLE public.subscription_charges OWNER TO "user";

--
-- Name: subscription_charges_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.subscription_charges_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_charges_id_seq OWNER TO "user";

--
-- Name: subscription_charges_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.subscription_charges_id_seq OWNED BY public.subscription_charges.id;


--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.subscriptions (
    id integer NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    status public.subscriptionstatus NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    product_id integer NOT NULL,
    user_id integer NOT NULL,
    payment_id integer
);


ALTER TABLE public.subscriptions OWNER TO "user";

--
-- Name: subscriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.subscriptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscriptions_id_seq OWNER TO "user";

--
-- Name: subscriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.subscriptions_id_seq OWNED BY public.subscriptions.id;


--
-- Name: telegram_users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.telegram_users (
    telegram_id bigint NOT NULL,
    is_admin boolean NOT NULL,
    is_handle boolean DEFAULT false NOT NULL,
    username character varying,
    referrer_id integer,
    id integer NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);


ALTER TABLE public.telegram_users OWNER TO "user";

--
-- Name: telegram_users_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.telegram_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.telegram_users_id_seq OWNER TO "user";

--
-- Name: telegram_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.telegram_users_id_seq OWNED BY public.telegram_users.id;


--
-- Name: configs id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.configs ALTER COLUMN id SET DEFAULT nextval('public.configs_id_seq'::regclass);


--
-- Name: finance_accounts id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.finance_accounts ALTER COLUMN id SET DEFAULT nextval('public.finance_accounts_id_seq'::regclass);


--
-- Name: moderators id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.moderators ALTER COLUMN id SET DEFAULT nextval('public.moderators_id_seq'::regclass);


--
-- Name: payment_receipts id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payment_receipts ALTER COLUMN id SET DEFAULT nextval('public.payment_receipts_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: server_configs id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_configs ALTER COLUMN id SET DEFAULT nextval('public.server_configs_id_seq'::regclass);


--
-- Name: servers id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.servers ALTER COLUMN id SET DEFAULT nextval('public.servers_id_seq'::regclass);


--
-- Name: subscription_charges id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscription_charges ALTER COLUMN id SET DEFAULT nextval('public.subscription_charges_id_seq'::regclass);


--
-- Name: subscriptions id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscriptions ALTER COLUMN id SET DEFAULT nextval('public.subscriptions_id_seq'::regclass);


--
-- Name: telegram_users id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.telegram_users ALTER COLUMN id SET DEFAULT nextval('public.telegram_users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.alembic_version (version_num) FROM stdin;
840e829b9262
\.


--
-- Data for Name: configs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.configs (name, uuid, config, id, created_at, updated_at, server_id, user_id) FROM stdin;
admin-1	3b5d3b51-affe-4dca-8691-ce166975a952	vless://3b5d3b51-affe-4dca-8691-ce166975a952@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#admin-1@user.id	7	2025-08-13 23:54:54.146506	2025-08-13 23:54:54.146506	1	1
diba-1	28ab93da-07b9-4246-ae33-23ada047d6cc	vless://28ab93da-07b9-4246-ae33-23ada047d6cc@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#diba-1@user.id	17	2025-08-14 15:04:04.413767	2025-08-14 15:04:04.413767	1	1
diba-2	64a9c74f-11df-46b6-978e-d066914bb77b	vless://64a9c74f-11df-46b6-978e-d066914bb77b@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#diba-2@user.id	18	2025-08-14 15:04:17.920566	2025-08-14 15:04:17.920566	1	1
dima-1	69cabc29-51db-42d7-a30b-385df8eff1d9	vless://69cabc29-51db-42d7-a30b-385df8eff1d9@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#dima-1@user.id	20	2025-08-14 19:35:09.803065	2025-08-14 19:35:09.803065	1	3
dima-ref-1-1	7f94f012-6606-483f-8a4f-7f205f10f6cb	vless://7f94f012-6606-483f-8a4f-7f205f10f6cb@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#dima-ref-1-1@user.id	22	2025-08-15 15:13:51.423953	2025-08-15 15:13:51.423953	1	1
biletskaya-1	266573dc-8968-45b3-9793-60bbd8aa2bfb	vless://266573dc-8968-45b3-9793-60bbd8aa2bfb@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#biletskaya-1@user.id	6	2025-08-13 23:54:07.943105	2025-08-13 23:54:07.943105	1	7
biletskaya-2	7835aa7f-8fda-49b0-a69c-40e6a9eb6e06	vless://7835aa7f-8fda-49b0-a69c-40e6a9eb6e06@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#biletskaya-2@user.id	23	2025-08-16 21:13:32.946409	2025-08-16 21:13:32.946409	1	7
Baksik2024-1	547bb042-6fdf-441e-a9ac-958dcd7d0e6a	vless://547bb042-6fdf-441e-a9ac-958dcd7d0e6a@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#Baksik2024-1@user.id	14	2025-08-14 08:48:44.5922	2025-08-14 08:48:44.5922	1	11
tolstbb-1	4a3a433d-ecab-4ab1-b6ce-ad708a860502	vless://4a3a433d-ecab-4ab1-b6ce-ad708a860502@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#tolstbb-1@user.id	11	2025-08-14 07:38:35.19879	2025-08-14 07:38:35.19879	1	8
OgPiSs1-1	5aa72e79-9617-46c2-b83b-0dd377ac46b3	vless://5aa72e79-9617-46c2-b83b-0dd377ac46b3@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#OgPiSs1-1@user.id	12	2025-08-14 07:50:08.973812	2025-08-14 07:50:08.973812	1	10
diba-3	8af42c62-4e4b-4070-805e-a768ead4d3ab	vless://8af42c62-4e4b-4070-805e-a768ead4d3ab@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#diba-3@user.id	19	2025-08-14 15:04:33.406742	2025-08-14 15:04:33.406742	1	1
ARGSENTINEL-1	5104fcc1-d9fa-4b12-8dbf-05fdcc2dc62f	vless://5104fcc1-d9fa-4b12-8dbf-05fdcc2dc62f@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#ARGSENTINEL-1@user.id	8	2025-08-14 07:07:23.212343	2025-08-14 07:07:23.212343	1	12
Tlufier-1	8e7f4c35-719f-462a-a866-0165d0c4b1f5	vless://8e7f4c35-719f-462a-a866-0165d0c4b1f5@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#Tlufier-1@user.id	16	2025-08-14 11:34:57.045671	2025-08-14 11:34:57.045671	1	13
vlxdislxve-1	d39d9d9e-f627-430a-938f-d1360834b6cd	vless://d39d9d9e-f627-430a-938f-d1360834b6cd@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#vlxdislxve-1@user.id	9	2025-08-14 07:08:34.624956	2025-08-14 07:08:34.624956	1	14
@Ktololp	594625e6-06f4-4985-8355-df240b401f0a	vless://594625e6-06f4-4985-8355-df240b401f0a@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#@Ktololp@user.id	10	2025-08-14 07:09:02.732755	2025-08-14 07:09:02.732755	1	15
dliaelki-1	f3d89ba2-f156-4b09-8313-154556249f4b	vless://f3d89ba2-f156-4b09-8313-154556249f4b@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#dliaelki-1@user.id	25	2025-08-20 11:17:33.851646	2025-08-20 11:17:33.851646	1	16
bad-sop1ay-1	b7be1772-dc00-4ac8-a2b4-987bab365d35	vless://b7be1772-dc00-4ac8-a2b4-987bab365d35@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#bad-sop1ay-1@user.id	26	2025-08-20 11:29:13.78599	2025-08-20 11:29:13.78599	1	9
bad_sop1ay-1	cc19a79c-79a6-499b-abe2-064e28aec4fb	vless://cc19a79c-79a6-499b-abe2-064e28aec4fb@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#bad_sop1ay-1@user.id	24	2025-08-20 10:24:13.497821	2025-08-20 10:24:13.497821	1	6
mid_lyn-1	850b94f9-1833-4004-a5eb-dae7e94f4fdf	vless://850b94f9-1833-4004-a5eb-dae7e94f4fdf@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#mid_lyn-1@user.id	15	2025-08-14 09:45:08.554798	2025-08-14 09:45:08.554798	1	17
sosunok-1	1fee2afa-2bd3-4d0b-b0b6-e08954295386	vless://1fee2afa-2bd3-4d0b-b0b6-e08954295386@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#sosunok-1@user.id	27	2025-08-20 15:10:11.689192	2025-08-20 15:10:11.689192	1	19
dobri-1	ae89586e-cf48-4c95-b225-a1f2ea41faeb	vless://ae89586e-cf48-4c95-b225-a1f2ea41faeb@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#dobri-1@user.id	21	2025-08-15 07:43:45.882814	2025-08-15 07:43:45.882814	1	18
kultyschev10-1	4102341a-d670-49f9-b511-01c787a6e51f	vless://4102341a-d670-49f9-b511-01c787a6e51f@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#kultyschev10-1@user.id	29	2025-08-20 15:18:18.895413	2025-08-20 15:18:18.895413	1	20
\.


--
-- Data for Name: finance_accounts; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.finance_accounts (id, balance, referral_percent, created_at, updated_at, user_id) FROM stdin;
2	0	15	2025-08-14 15:58:23.257356	2025-08-14 15:58:23.257356	2
3	0	25	2025-08-14 19:34:11.20645	2025-08-14 19:34:11.20645	3
5	0	15	2025-08-15 00:40:27.241361	2025-08-15 00:40:27.241361	5
4	500.15	15	2025-08-14 23:52:36.10777	2025-08-15 00:49:52.568576	4
6	1	15	2025-08-15 00:46:08.105451	2025-08-15 00:51:03.596457	6
1	30059936.349999998	15	2025-08-13 23:13:33.449359	2025-08-15 00:51:03.626784	1
7	0	15	2025-08-16 21:12:49.078446	2025-08-16 21:12:49.078446	7
8	0	15	2025-08-20 10:17:06.107195	2025-08-20 10:17:06.107195	8
9	0	15	2025-08-20 10:21:43.513569	2025-08-20 10:21:43.513569	9
10	0	15	2025-08-20 10:32:00.60249	2025-08-20 10:32:00.60249	10
11	0	15	2025-08-20 10:51:53.081037	2025-08-20 10:51:53.081037	11
12	0	15	2025-08-20 10:59:27.587731	2025-08-20 10:59:27.587731	12
13	0	15	2025-08-20 11:03:35.281316	2025-08-20 11:03:35.281316	13
14	0	15	2025-08-20 11:04:03.863229	2025-08-20 11:04:03.863229	14
15	0	15	2025-08-20 11:05:13.64495	2025-08-20 11:05:13.64495	15
16	0	15	2025-08-20 11:16:35.221185	2025-08-20 11:16:35.221185	16
17	0	15	2025-08-20 12:16:52.95124	2025-08-20 12:16:52.95124	17
18	0	15	2025-08-20 14:14:11.077389	2025-08-20 14:14:11.077389	18
19	0	15	2025-08-20 15:09:05.236255	2025-08-20 15:09:05.236255	19
20	0	15	2025-08-20 15:17:13.232688	2025-08-20 15:17:13.232688	20
\.


--
-- Data for Name: moderators; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.moderators (id, created_at, updated_at, user_id) FROM stdin;
1	2025-08-14 20:29:10.418425	2025-08-14 20:29:10.418425	1
\.


--
-- Data for Name: payment_receipts; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.payment_receipts (id, file_path, filename, created_at, updated_at, payment_id) FROM stdin;
1	uploads/receipts/5/713237f6-2c86-4eb5-a130-528aea682a73.jpg	713237f6-2c86-4eb5-a130-528aea682a73.jpg	2025-08-14 20:28:43.951155	2025-08-14 20:28:43.951155	5
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.payments (id, amount, transaction_type, status, mode, payment_method, external_id, note, created_at, updated_at, finance_account_id) FROM stdin;
1	10000	deposit	pending	production	system	\N	\N	2025-08-14 16:40:50.9379	2025-08-14 16:40:50.9379	1
2	100000	deposit	pending	production	handle	\N	\N	2025-08-14 16:41:14.120164	2025-08-14 16:41:14.120164	1
3	1000	deposit	pending	production	crypto	720681	\N	2025-08-14 17:40:48.457761	2025-08-14 17:40:48.86142	1
4	1000	deposit	pending	production	system	\N	\N	2025-08-14 19:31:18.610261	2025-08-14 19:31:18.610261	1
5	1000	deposit	completed	production	handle	\N	\N	2025-08-14 20:28:37.925634	2025-08-14 20:29:20.747394	1
6	500	deposit	failed	production	crypto	720830	\N	2025-08-14 23:53:14.904278	2025-08-14 23:53:52.100252	4
7	500	deposit	failed	production	crypto	720831	\N	2025-08-14 23:54:45.796852	2025-08-14 23:54:49.854394	4
8	500	deposit	failed	production	crypto	720832	\N	2025-08-14 23:55:26.602188	2025-08-14 23:55:32.436563	4
9	5e+20	deposit	pending	production	crypto	\N	\N	2025-08-14 23:56:13.908085	2025-08-14 23:56:13.908085	4
10	99999	deposit	failed	production	crypto	720833	\N	2025-08-14 23:56:37.768128	2025-08-14 23:56:56.509875	4
11	90909	deposit	failed	production	crypto	720834	\N	2025-08-14 23:58:54.97539	2025-08-15 00:06:06.450525	4
12	500	deposit	failed	production	crypto	720836	\N	2025-08-15 00:16:04.228821	2025-08-15 00:16:07.347245	4
13	500	deposit	completed	production	crypto	720837	\N	2025-08-15 00:16:19.324315	2025-08-15 00:19:07.869024	4
14	6000000000	deposit	pending	production	crypto	\N	\N	2025-08-15 00:28:28.602994	2025-08-15 00:28:28.602994	4
15	0	deposit	pending	production	crypto	\N	\N	2025-08-15 00:29:01.049554	2025-08-15 00:29:01.049554	4
16	1	deposit	failed	production	crypto	720838	\N	2025-08-15 00:29:09.307089	2025-08-15 00:29:30.490629	4
17	0	deposit	pending	production	crypto	\N	\N	2025-08-15 00:29:39.307483	2025-08-15 00:29:39.307483	4
18	0	deposit	pending	production	crypto	\N	\N	2025-08-15 00:29:47.531198	2025-08-15 00:29:47.531198	4
19	0	deposit	pending	production	crypto	\N	\N	2025-08-15 00:29:52.212499	2025-08-15 00:29:52.212499	4
20	1	deposit	pending	production	crypto	720841	\N	2025-08-15 00:41:23.317958	2025-08-15 00:41:23.704498	5
21	100	deposit	failed	production	crypto	720842	\N	2025-08-15 00:45:02.409624	2025-08-15 00:45:15.430276	5
22	199999999	deposit	failed	production	crypto	720843	\N	2025-08-15 00:48:21.253785	2025-08-15 00:48:34.395108	6
23	0	deposit	pending	production	crypto	\N	\N	2025-08-15 00:49:41.321034	2025-08-15 00:49:41.321034	5
24	1	deposit	pending	production	crypto	720844	\N	2025-08-15 00:49:47.558787	2025-08-15 00:49:47.870213	5
25	0	deposit	pending	production	crypto	\N	\N	2025-08-15 00:49:50.98169	2025-08-15 00:49:50.98169	6
26	1	deposit	completed	production	crypto	720846	\N	2025-08-15 00:50:29.929481	2025-08-15 00:51:03.606779	6
27	200000	deposit	pending	production	crypto	720848	\N	2025-08-15 00:51:22.643419	2025-08-15 00:51:22.980975	5
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.products (price, product_type, id, name, duration_days, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: server_configs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.server_configs (id, public_key, private_key, config_data, created_at, updated_at, server_id) FROM stdin;
1	PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I	0NQ5SMrEcfaniH7Sn1NC16lwVkXuSK2FbR38gYWsA0Q	{"log": {"loglevel": "warning"}, "inbounds": [{"port": 44344, "protocol": "vless", "settings": {"clients": [{"id": "cbabcd4b-1585-4f44-9f87-3a2e888c19c8", "flow": "xtls-rprx-vision", "level": 0, "email": "admin_init@xray"}, {"email": "she1kopr9d-1@user.id", "id": "b5f1932c-af36-4df0-8780-c7e662e7e064", "flow": "xtls-rprx-vision", "level": 0}, {"email": "she1kopr9d-2@user.id", "id": "d51d540c-bbf1-4f97-a456-915f2b2548c4", "flow": "xtls-rprx-vision", "level": 0}, {"email": "test@user.id", "id": "e4e685e5-075b-457b-9dbe-7d50c3c71d2a", "flow": "xtls-rprx-vision", "level": 0}, {"email": "test2@user.id", "id": "a7056b3c-b7c5-486d-ba2e-5c2868021703", "flow": "xtls-rprx-vision", "level": 0}, {"email": "biletskaya-1@user.id", "id": "266573dc-8968-45b3-9793-60bbd8aa2bfb", "flow": "xtls-rprx-vision", "level": 0}, {"email": "admin-1@user.id", "id": "3b5d3b51-affe-4dca-8691-ce166975a952", "flow": "xtls-rprx-vision", "level": 0}, {"email": "ARGSENTINEL-1@user.id", "id": "5104fcc1-d9fa-4b12-8dbf-05fdcc2dc62f", "flow": "xtls-rprx-vision", "level": 0}, {"email": "vlxdislxve-1@user.id", "id": "d39d9d9e-f627-430a-938f-d1360834b6cd", "flow": "xtls-rprx-vision", "level": 0}, {"email": "@Ktololp@user.id", "id": "594625e6-06f4-4985-8355-df240b401f0a", "flow": "xtls-rprx-vision", "level": 0}, {"email": "tolstbb-1@user.id", "id": "4a3a433d-ecab-4ab1-b6ce-ad708a860502", "flow": "xtls-rprx-vision", "level": 0}, {"email": "OgPiSs1-1@user.id", "id": "5aa72e79-9617-46c2-b83b-0dd377ac46b3", "flow": "xtls-rprx-vision", "level": 0}, {"email": "admin-android-1@user.id", "id": "fb578fe9-3f66-43a5-8af1-b96e5a1a8b8f", "flow": "xtls-rprx-vision", "level": 0}, {"email": "Baksik2024-1@user.id", "id": "547bb042-6fdf-441e-a9ac-958dcd7d0e6a", "flow": "xtls-rprx-vision", "level": 0}, {"email": "mid_lyn-1@user.id", "id": "850b94f9-1833-4004-a5eb-dae7e94f4fdf", "flow": "xtls-rprx-vision", "level": 0}, {"email": "Tlufier-1@user.id", "id": "8e7f4c35-719f-462a-a866-0165d0c4b1f5", "flow": "xtls-rprx-vision", "level": 0}, {"email": "diba-1@user.id", "id": "28ab93da-07b9-4246-ae33-23ada047d6cc", "flow": "xtls-rprx-vision", "level": 0}, {"email": "diba-2@user.id", "id": "64a9c74f-11df-46b6-978e-d066914bb77b", "flow": "xtls-rprx-vision", "level": 0}, {"email": "diba-3@user.id", "id": "8af42c62-4e4b-4070-805e-a768ead4d3ab", "flow": "xtls-rprx-vision", "level": 0}, {"email": "dima-1@user.id", "id": "69cabc29-51db-42d7-a30b-385df8eff1d9", "flow": "xtls-rprx-vision", "level": 0}, {"email": "dobri-1@user.id", "id": "ae89586e-cf48-4c95-b225-a1f2ea41faeb", "flow": "xtls-rprx-vision", "level": 0}, {"email": "dima-ref-1-1@user.id", "id": "7f94f012-6606-483f-8a4f-7f205f10f6cb", "flow": "xtls-rprx-vision", "level": 0}, {"email": "biletskaya-2@user.id", "id": "7835aa7f-8fda-49b0-a69c-40e6a9eb6e06", "flow": "xtls-rprx-vision", "level": 0}, {"email": "bad_sop1ay-1@user.id", "id": "cc19a79c-79a6-499b-abe2-064e28aec4fb", "flow": "xtls-rprx-vision", "level": 0}, {"email": "dliaelki-1@user.id", "id": "f3d89ba2-f156-4b09-8313-154556249f4b", "flow": "xtls-rprx-vision", "level": 0}, {"email": "bad-sop1ay-1@user.id", "id": "b7be1772-dc00-4ac8-a2b4-987bab365d35", "flow": "xtls-rprx-vision", "level": 0}, {"email": "sosunok-1@user.id", "id": "1fee2afa-2bd3-4d0b-b0b6-e08954295386", "flow": "xtls-rprx-vision", "level": 0}, {"email": "jelyfishron-1@user.id", "id": "6e63fd66-93b7-4ab9-bc81-727b4fc4ba52", "flow": "xtls-rprx-vision", "level": 0}, {"email": "kultyschev10-1@user.id", "id": "4102341a-d670-49f9-b511-01c787a6e51f", "flow": "xtls-rprx-vision", "level": 0}], "decryption": "none"}, "streamSettings": {"network": "tcp", "security": "reality", "realitySettings": {"show": false, "dest": "www.cloudflare.com:443", "xver": 0, "serverNames": ["www.cloudflare.com"], "privateKey": "0NQ5SMrEcfaniH7Sn1NC16lwVkXuSK2FbR38gYWsA0Q", "shortIds": ["12345678"]}}}], "outbounds": [{"protocol": "freedom"}, {"protocol": "blackhole", "settings": {}, "tag": "blocked"}], "routing": {"rules": [{"type": "field", "ip": ["geoip:private"], "outboundTag": "blocked"}]}}	2025-08-13 23:14:57.740754	2025-08-20 15:18:18.92625	1
\.


--
-- Data for Name: servers; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.servers (name, code, id) FROM stdin;
GRM-2	GRM-2:qwerty.1	1
\.


--
-- Data for Name: subscription_charges; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.subscription_charges (id, created_at, updated_at, subscription_id, payment_id) FROM stdin;
\.


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.subscriptions (id, start_date, end_date, status, created_at, updated_at, product_id, user_id, payment_id) FROM stdin;
\.


--
-- Data for Name: telegram_users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.telegram_users (telegram_id, is_admin, is_handle, username, referrer_id, id, created_at, updated_at) FROM stdin;
798030433	t	t	she1kopr9d	\N	1	2025-08-13 23:13:33.435437	2025-08-13 23:13:33.435437
5805129073	f	f	bcImmammahappyyy	1	2	2025-08-14 15:58:23.220342	2025-08-14 15:58:23.220342
5325094036	f	f	ImBigPeka	1	3	2025-08-14 19:34:11.193023	2025-08-14 19:34:11.193023
7717483630	f	f	Krobitik	1	4	2025-08-14 23:52:36.091653	2025-08-14 23:52:36.091653
7857810365	f	f	superundergroundchelll	1	6	2025-08-15 00:46:08.098206	2025-08-15 00:46:08.098206
6302532186	f	f	bog1dan1	4	5	2025-08-15 00:40:27.217486	2025-08-15 00:40:27.217486
949796701	f	f	wtkitty	1	7	2025-08-16 21:12:49.055217	2025-08-16 21:12:49.055217
1055343140	f	f	bad_sop1ay	8	9	2025-08-20 10:21:43.489833	2025-08-20 10:21:43.489833
801700485	f	f	tolstbb	1	8	2025-08-20 10:17:06.0884	2025-08-20 10:17:06.0884
575216295	f	f	OgPiSs1	1	10	2025-08-20 10:32:00.592123	2025-08-20 10:32:00.592123
2022039753	f	f	Baksik2024	1	11	2025-08-20 10:51:53.063019	2025-08-20 10:51:53.063019
5654028155	f	f	ARGSENTINEL	1	12	2025-08-20 10:59:27.579132	2025-08-20 10:59:27.579132
1048975878	f	f	Tlufier	1	13	2025-08-20 11:03:35.269895	2025-08-20 11:03:35.269895
896475099	f	f	vlxdislxve	1	14	2025-08-20 11:04:03.85434	2025-08-20 11:04:03.85434
810285026	f	f	Ktololp	1	15	2025-08-20 11:05:13.635526	2025-08-20 11:05:13.635526
7531328517	f	f	dliaelki	1	16	2025-08-20 11:16:35.21001	2025-08-20 11:16:35.21001
1017871562	f	f	mid_lyn	1	17	2025-08-20 12:16:52.940243	2025-08-20 12:16:52.940243
1359560791	f	f	jelyfishron	1	18	2025-08-20 14:14:11.061735	2025-08-20 14:14:11.061735
415597121	f	f	danyaxe	1	19	2025-08-20 15:09:05.225211	2025-08-20 15:09:05.225211
1096920627	f	f	kultyschev10	1	20	2025-08-20 15:17:13.220997	2025-08-20 15:17:13.220997
\.


--
-- Name: configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.configs_id_seq', 29, true);


--
-- Name: finance_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.finance_accounts_id_seq', 20, true);


--
-- Name: moderators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.moderators_id_seq', 1, true);


--
-- Name: payment_receipts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.payment_receipts_id_seq', 1, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.payments_id_seq', 27, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.products_id_seq', 1, false);


--
-- Name: server_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.server_configs_id_seq', 1, true);


--
-- Name: servers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.servers_id_seq', 1, true);


--
-- Name: subscription_charges_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.subscription_charges_id_seq', 1, false);


--
-- Name: subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.subscriptions_id_seq', 1, false);


--
-- Name: telegram_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.telegram_users_id_seq', 20, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: configs configs_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.configs
    ADD CONSTRAINT configs_pkey PRIMARY KEY (id);


--
-- Name: finance_accounts finance_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.finance_accounts
    ADD CONSTRAINT finance_accounts_pkey PRIMARY KEY (id);


--
-- Name: moderators moderators_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.moderators
    ADD CONSTRAINT moderators_pkey PRIMARY KEY (id);


--
-- Name: moderators moderators_user_id_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.moderators
    ADD CONSTRAINT moderators_user_id_key UNIQUE (user_id);


--
-- Name: payment_receipts payment_receipts_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payment_receipts
    ADD CONSTRAINT payment_receipts_pkey PRIMARY KEY (id);


--
-- Name: payments payments_external_id_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_external_id_key UNIQUE (external_id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: server_configs server_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_configs
    ADD CONSTRAINT server_configs_pkey PRIMARY KEY (id);


--
-- Name: server_configs server_configs_server_id_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_configs
    ADD CONSTRAINT server_configs_server_id_key UNIQUE (server_id);


--
-- Name: servers servers_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.servers
    ADD CONSTRAINT servers_pkey PRIMARY KEY (id);


--
-- Name: subscription_charges subscription_charges_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscription_charges
    ADD CONSTRAINT subscription_charges_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: telegram_users telegram_users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.telegram_users
    ADD CONSTRAINT telegram_users_pkey PRIMARY KEY (id);


--
-- Name: telegram_users telegram_users_telegram_id_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.telegram_users
    ADD CONSTRAINT telegram_users_telegram_id_key UNIQUE (telegram_id);


--
-- Name: configs configs_server_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.configs
    ADD CONSTRAINT configs_server_id_fkey FOREIGN KEY (server_id) REFERENCES public.servers(id);


--
-- Name: configs configs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.configs
    ADD CONSTRAINT configs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.telegram_users(id);


--
-- Name: finance_accounts finance_accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.finance_accounts
    ADD CONSTRAINT finance_accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.telegram_users(id);


--
-- Name: moderators moderators_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.moderators
    ADD CONSTRAINT moderators_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.telegram_users(id);


--
-- Name: payment_receipts payment_receipts_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payment_receipts
    ADD CONSTRAINT payment_receipts_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: payments payments_finance_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_finance_account_id_fkey FOREIGN KEY (finance_account_id) REFERENCES public.finance_accounts(id);


--
-- Name: server_configs server_configs_server_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.server_configs
    ADD CONSTRAINT server_configs_server_id_fkey FOREIGN KEY (server_id) REFERENCES public.servers(id);


--
-- Name: subscription_charges subscription_charges_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscription_charges
    ADD CONSTRAINT subscription_charges_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: subscription_charges subscription_charges_subscription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscription_charges
    ADD CONSTRAINT subscription_charges_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES public.subscriptions(id);


--
-- Name: subscriptions subscriptions_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: subscriptions subscriptions_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: subscriptions subscriptions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.telegram_users(id);


--
-- Name: telegram_users telegram_users_referrer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.telegram_users
    ADD CONSTRAINT telegram_users_referrer_id_fkey FOREIGN KEY (referrer_id) REFERENCES public.telegram_users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict zQVVgixVcq6LQfUWgZpCYChEWCIXrR4JlwJAJSNKmhpr6SzAorqZzr86oMWRlUr

