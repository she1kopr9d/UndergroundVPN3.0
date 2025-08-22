--
-- PostgreSQL database dump
--

\restrict 11niJaGVjL76rvugDnUa9bcyU5FzhZ5GoflH26AOsxsRa5SKzH98E2TS2TGVkvP

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
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
-- Name: execute_products; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.execute_products (
    id integer NOT NULL,
    executor_name character varying NOT NULL,
    product_id integer NOT NULL
);


ALTER TABLE public.execute_products OWNER TO "user";

--
-- Name: execute_products_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.execute_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.execute_products_id_seq OWNER TO "user";

--
-- Name: execute_products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.execute_products_id_seq OWNED BY public.execute_products.id;


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
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    is_friend boolean DEFAULT false NOT NULL
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
    payment_id integer,
    external_id integer
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
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    is_friend boolean DEFAULT false NOT NULL
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
-- Name: execute_products id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.execute_products ALTER COLUMN id SET DEFAULT nextval('public.execute_products_id_seq'::regclass);


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
ae9f64ee9af2
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
mid_lyn-1	850b94f9-1833-4004-a5eb-dae7e94f4fdf	vless://850b94f9-1833-4004-a5eb-dae7e94f4fdf@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#mid_lyn-1@user.id	15	2025-08-14 09:45:08.554798	2025-08-14 09:45:08.554798	1	17
dobri-1	ae89586e-cf48-4c95-b225-a1f2ea41faeb	vless://ae89586e-cf48-4c95-b225-a1f2ea41faeb@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#dobri-1@user.id	21	2025-08-15 07:43:45.882814	2025-08-15 07:43:45.882814	1	18
kultyschev10-1	4102341a-d670-49f9-b511-01c787a6e51f	vless://4102341a-d670-49f9-b511-01c787a6e51f@79.132.143.35:44344?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.cloudflare.com&fp=chrome&pbk=PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I&sid=12345678&type=tcp#kultyschev10-1@user.id	29	2025-08-20 15:18:18.895413	2025-08-20 15:18:18.895413	1	20
\.


--
-- Data for Name: execute_products; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.execute_products (id, executor_name, product_id) FROM stdin;
1	vpn_30_day	1
2	vpn_90_day	2
3	vpn_30_day	3
\.


--
-- Data for Name: finance_accounts; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.finance_accounts (id, balance, referral_percent, created_at, updated_at, user_id) FROM stdin;
2	0	15	2025-08-14 15:58:23.257356	2025-08-14 15:58:23.257356	2
3	0	25	2025-08-14 19:34:11.20645	2025-08-14 19:34:11.20645	3
5	0	15	2025-08-15 00:40:27.241361	2025-08-15 00:40:27.241361	5
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
20	0	15	2025-08-20 15:17:13.232688	2025-08-20 15:17:13.232688	20
4	0	15	2025-08-14 23:52:36.10777	2025-08-15 00:49:52.568576	4
19	0	15	2025-08-20 15:09:05.236255	2025-08-21 19:00:33.122467	19
21	0	15	2025-08-22 11:44:59.637269	2025-08-22 11:44:59.637269	21
1	95812	15	2025-08-13 23:13:33.449359	2025-08-22 12:35:22.256037	1
22	0	15	2025-08-22 14:11:21.799052	2025-08-22 14:11:21.799052	22
\.


--
-- Data for Name: moderators; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.moderators (id, created_at, updated_at, user_id) FROM stdin;
1	2025-08-14 20:29:10.418425	2025-08-14 20:29:10.418425	1
2	2025-08-22 11:45:29.848537	2025-08-22 11:45:29.848537	21
\.


--
-- Data for Name: payment_receipts; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.payment_receipts (id, file_path, filename, created_at, updated_at, payment_id) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.payments (id, amount, transaction_type, status, mode, payment_method, external_id, note, created_at, updated_at, finance_account_id) FROM stdin;
58	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:24:11.186412	2025-08-22 12:24:11.19774	1
59	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:28:09.082109	2025-08-22 12:28:09.102596	1
60	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:35:22.239322	2025-08-22 12:35:22.260494	1
51	100	withdrawal	completed	production	system	\N	\N	2025-08-22 11:59:41.637418	2025-08-22 11:59:41.647398	1
52	499	withdrawal	completed	production	system	\N	\N	2025-08-22 12:22:14.723931	2025-08-22 12:22:14.73855	1
53	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:23:35.110564	2025-08-22 12:23:35.122337	1
54	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:23:41.045424	2025-08-22 12:23:41.055287	1
55	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:23:48.270989	2025-08-22 12:23:48.282784	1
56	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:23:56.317225	2025-08-22 12:23:56.32764	1
57	199	withdrawal	completed	production	system	\N	\N	2025-08-22 12:24:05.682396	2025-08-22 12:24:05.691811	1
43	499	withdrawal	completed	production	system	\N	\N	2025-08-22 11:55:17.169794	2025-08-22 11:55:17.190564	1
44	499	withdrawal	completed	production	system	\N	\N	2025-08-22 11:55:26.643828	2025-08-22 11:55:26.656149	1
45	499	withdrawal	completed	production	system	\N	\N	2025-08-22 11:55:39.641768	2025-08-22 11:55:39.650726	1
46	100	withdrawal	completed	production	system	\N	\N	2025-08-22 11:58:59.273633	2025-08-22 11:58:59.287875	1
47	100	withdrawal	completed	production	system	\N	\N	2025-08-22 11:59:08.621343	2025-08-22 11:59:08.635506	1
48	100	withdrawal	completed	production	system	\N	\N	2025-08-22 11:59:15.054394	2025-08-22 11:59:15.062748	1
49	100	withdrawal	completed	production	system	\N	\N	2025-08-22 11:59:22.478176	2025-08-22 11:59:22.485848	1
50	100	withdrawal	completed	production	system	\N	\N	2025-08-22 11:59:33.768676	2025-08-22 11:59:33.780045	1
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.products (price, product_type, id, name, duration_days, created_at, updated_at, is_friend) FROM stdin;
199.00	recurring	1	Открытый интернет на 30 дней | 1 клиент	30	2025-08-21 16:59:32.545188	2025-08-21 16:59:32.545188	f
499.00	recurring	2	Открытый интернет на 90 дней | 1 клиент	90	2025-08-21 17:00:13.258051	2025-08-21 17:00:13.258051	f
100.00	recurring	3	[Друг] Открытый интернет на 30 дней | 1 конфиг	30	2025-08-21 22:33:47.65705	2025-08-21 22:33:47.65705	t
\.


--
-- Data for Name: server_configs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.server_configs (id, public_key, private_key, config_data, created_at, updated_at, server_id) FROM stdin;
1	PbiGSA6zBYZwJ9-_g95wijyHliFggAAghOU-ygXvH0I	0NQ5SMrEcfaniH7Sn1NC16lwVkXuSK2FbR38gYWsA0Q	{\n    "log": {\n        "loglevel": "warning"\n    },\n    "inbounds": [\n        {\n            "port": 44344,\n            "protocol": "vless",\n            "settings": {\n                "clients": [\n                    {\n                        "id": "cbabcd4b-1585-4f44-9f87-3a2e888c19c8",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0,\n                        "email": "admin_init@xray"\n                    },\n                    {\n                        "email": "she1kopr9d-1@user.id",\n                        "id": "b5f1932c-af36-4df0-8780-c7e662e7e064",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "she1kopr9d-2@user.id",\n                        "id": "d51d540c-bbf1-4f97-a456-915f2b2548c4",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "test@user.id",\n                        "id": "e4e685e5-075b-457b-9dbe-7d50c3c71d2a",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "test2@user.id",\n                        "id": "a7056b3c-b7c5-486d-ba2e-5c2868021703",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "biletskaya-1@user.id",\n                        "id": "266573dc-8968-45b3-9793-60bbd8aa2bfb",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "admin-1@user.id",\n                        "id": "3b5d3b51-affe-4dca-8691-ce166975a952",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "ARGSENTINEL-1@user.id",\n                        "id": "5104fcc1-d9fa-4b12-8dbf-05fdcc2dc62f",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "vlxdislxve-1@user.id",\n                        "id": "d39d9d9e-f627-430a-938f-d1360834b6cd",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "@Ktololp@user.id",\n                        "id": "594625e6-06f4-4985-8355-df240b401f0a",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "tolstbb-1@user.id",\n                        "id": "4a3a433d-ecab-4ab1-b6ce-ad708a860502",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "OgPiSs1-1@user.id",\n                        "id": "5aa72e79-9617-46c2-b83b-0dd377ac46b3",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "admin-android-1@user.id",\n                        "id": "fb578fe9-3f66-43a5-8af1-b96e5a1a8b8f",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "Baksik2024-1@user.id",\n                        "id": "547bb042-6fdf-441e-a9ac-958dcd7d0e6a",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "mid_lyn-1@user.id",\n                        "id": "850b94f9-1833-4004-a5eb-dae7e94f4fdf",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "Tlufier-1@user.id",\n                        "id": "8e7f4c35-719f-462a-a866-0165d0c4b1f5",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "diba-1@user.id",\n                        "id": "28ab93da-07b9-4246-ae33-23ada047d6cc",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "diba-2@user.id",\n                        "id": "64a9c74f-11df-46b6-978e-d066914bb77b",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "diba-3@user.id",\n                        "id": "8af42c62-4e4b-4070-805e-a768ead4d3ab",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "dima-1@user.id",\n                        "id": "69cabc29-51db-42d7-a30b-385df8eff1d9",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "dobri-1@user.id",\n                        "id": "ae89586e-cf48-4c95-b225-a1f2ea41faeb",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "dima-ref-1-1@user.id",\n                        "id": "7f94f012-6606-483f-8a4f-7f205f10f6cb",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "biletskaya-2@user.id",\n                        "id": "7835aa7f-8fda-49b0-a69c-40e6a9eb6e06",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "bad_sop1ay-1@user.id",\n                        "id": "cc19a79c-79a6-499b-abe2-064e28aec4fb",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "dliaelki-1@user.id",\n                        "id": "f3d89ba2-f156-4b09-8313-154556249f4b",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "bad-sop1ay-1@user.id",\n                        "id": "b7be1772-dc00-4ac8-a2b4-987bab365d35",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "sosunok-1@user.id",\n                        "id": "1fee2afa-2bd3-4d0b-b0b6-e08954295386",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "jelyfishron-1@user.id",\n                        "id": "6e63fd66-93b7-4ab9-bc81-727b4fc4ba52",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    },\n                    {\n                        "email": "kultyschev10-1@user.id",\n                        "id": "4102341a-d670-49f9-b511-01c787a6e51f",\n                        "flow": "xtls-rprx-vision",\n                        "level": 0\n                    }\n                ],\n                "decryption": "none"\n            },\n            "streamSettings": {\n                "network": "tcp",\n                "security": "reality",\n                "realitySettings": {\n                    "show": false,\n                    "dest": "www.cloudflare.com:443",\n                    "xver": 0,\n                    "serverNames": [\n                        "www.cloudflare.com"\n                    ],\n                    "privateKey": "0NQ5SMrEcfaniH7Sn1NC16lwVkXuSK2FbR38gYWsA0Q",\n                    "shortIds": [\n                        "12345678"\n                    ]\n                }\n            }\n        }\n    ],\n    "outbounds": [\n        {\n            "protocol": "freedom"\n        },\n        {\n            "protocol": "blackhole",\n            "settings": {},\n            "tag": "blocked"\n        }\n    ],\n    "routing": {\n        "rules": [\n            {\n                "type": "field",\n                "ip": [\n                    "geoip:private"\n                ],\n                "outboundTag": "blocked"\n            }\n        ]\n    }\n}	2025-08-13 23:14:57.740754	2025-08-22 13:51:42.076788	1
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
7	2025-08-22 11:55:17.205936	2025-08-22 11:55:17.205936	7	43
8	2025-08-22 11:55:26.666549	2025-08-22 11:55:26.666549	8	44
9	2025-08-22 11:55:39.659031	2025-08-22 11:55:39.659031	9	45
10	2025-08-22 11:58:59.298993	2025-08-22 11:58:59.298993	10	46
11	2025-08-22 11:59:08.643624	2025-08-22 11:59:08.643624	11	47
12	2025-08-22 11:59:15.070792	2025-08-22 11:59:15.070792	12	48
13	2025-08-22 11:59:22.494495	2025-08-22 11:59:22.494495	13	49
14	2025-08-22 11:59:33.7898	2025-08-22 11:59:33.7898	14	50
15	2025-08-22 11:59:41.656474	2025-08-22 11:59:41.656474	15	51
16	2025-08-22 12:22:14.74844	2025-08-22 12:22:14.74844	16	52
17	2025-08-22 12:23:35.130854	2025-08-22 12:23:35.130854	17	53
18	2025-08-22 12:23:41.062933	2025-08-22 12:23:41.062933	18	54
19	2025-08-22 12:23:48.29247	2025-08-22 12:23:48.29247	19	55
20	2025-08-22 12:23:56.336766	2025-08-22 12:23:56.336766	20	56
21	2025-08-22 12:24:05.700269	2025-08-22 12:24:05.700269	21	57
22	2025-08-22 12:24:11.20638	2025-08-22 12:24:11.20638	22	58
23	2025-08-22 12:28:09.115397	2025-08-22 12:28:09.115397	23	59
24	2025-08-22 12:35:22.269856	2025-08-22 12:35:22.269856	24	60
\.


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.subscriptions (id, start_date, end_date, status, created_at, updated_at, product_id, user_id, payment_id, external_id) FROM stdin;
17	2025-08-22 12:23:35.13002	2025-09-21 12:23:35.13002	active	2025-08-22 12:23:35.130854	2025-08-22 12:23:35.588178	1	9	53	26
18	2025-08-22 12:23:41.062272	2025-09-21 12:23:41.062272	active	2025-08-22 12:23:41.062933	2025-08-22 12:23:41.512314	1	13	54	16
19	2025-08-22 12:23:48.291526	2025-09-21 12:23:48.291526	active	2025-08-22 12:23:48.29247	2025-08-22 12:23:48.690274	1	12	55	8
20	2025-08-22 12:23:56.335984	2025-09-21 12:23:56.335984	active	2025-08-22 12:23:56.336766	2025-08-22 12:23:56.798225	1	20	56	29
21	2025-08-22 12:24:05.699384	2025-09-21 12:24:05.699384	active	2025-08-22 12:24:05.700269	2025-08-22 12:24:06.20342	1	8	57	11
22	2025-08-22 12:24:11.205604	2025-09-21 12:24:11.205604	active	2025-08-22 12:24:11.20638	2025-08-22 12:24:11.670191	1	11	58	14
23	2025-08-22 12:28:09.114443	2025-09-21 12:28:09.114443	active	2025-08-22 12:28:09.115397	2025-08-22 12:28:09.555051	1	1	59	22
7	2025-08-22 11:55:17.204347	2025-12-01 11:55:17.204347	active	2025-08-22 11:55:17.205936	2025-08-22 11:55:18.049076	2	1	43	17
8	2025-08-22 11:55:26.665574	2025-12-01 11:55:26.665574	active	2025-08-22 11:55:26.666549	2025-08-22 11:55:27.108764	2	1	44	18
9	2025-08-22 11:55:39.658244	2025-12-01 11:55:39.658244	active	2025-08-22 11:55:39.659031	2025-08-22 11:55:40.060734	2	1	45	19
24	2025-08-22 12:35:22.268578	2025-08-22 12:35:22.268578	expired	2025-08-22 12:35:22.269856	2025-08-22 12:35:54.885467	1	1	60	53
10	2025-08-22 11:58:59.298116	2025-10-01 11:58:59.298116	active	2025-08-22 11:58:59.298993	2025-08-22 11:58:59.685959	3	17	46	15
11	2025-08-22 11:59:08.642798	2025-10-01 11:59:08.642798	active	2025-08-22 11:59:08.643624	2025-08-22 11:59:09.084719	3	18	47	21
12	2025-08-22 11:59:15.070093	2025-10-01 11:59:08.642798	active	2025-08-22 11:59:15.070792	2025-08-22 11:59:15.372946	3	7	48	23
13	2025-08-22 11:59:22.493508	2025-10-01 11:59:08.642798	active	2025-08-22 11:59:22.494495	2025-08-22 11:59:22.824853	3	7	49	6
14	2025-08-22 11:59:33.788896	2025-10-01 11:59:08.642798	active	2025-08-22 11:59:33.7898	2025-08-22 11:59:34.101582	3	15	50	10
15	2025-08-22 11:59:41.655822	2025-10-01 11:59:08.642798	active	2025-08-22 11:59:41.656474	2025-08-22 11:59:42.030552	3	14	51	9
16	2025-08-22 12:22:14.747258	2025-11-20 12:22:14.747258	active	2025-08-22 12:22:14.74844	2025-08-22 12:22:15.173807	2	16	52	25
\.


--
-- Data for Name: telegram_users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.telegram_users (telegram_id, is_admin, is_handle, username, referrer_id, id, created_at, updated_at, is_friend) FROM stdin;
5325094036	f	f	ImBigPeka	1	3	2025-08-14 19:34:11.193023	2025-08-14 19:34:11.193023	f
6302532186	f	f	bog1dan1	4	5	2025-08-15 00:40:27.217486	2025-08-15 00:40:27.217486	f
798030433	t	t	she1kopr9d	\N	1	2025-08-13 23:13:33.435437	2025-08-13 23:13:33.435437	t
575216295	f	f	OgPiSs1	1	10	2025-08-20 10:32:00.592123	2025-08-20 10:32:00.592123	f
5805129073	f	f	bcImmammahappyyy	1	2	2025-08-14 15:58:23.220342	2025-08-14 15:58:23.220342	t
415597121	f	t	danyaxe	1	19	2025-08-20 15:09:05.225211	2025-08-21 18:54:00.662519	t
1055343140	f	t	bad_sop1ay	8	9	2025-08-20 10:21:43.489833	2025-08-20 10:21:43.489833	f
7531328517	f	t	dliaelki	14	16	2025-08-20 11:16:35.21001	2025-08-20 11:16:35.21001	f
1048975878	f	t	Tlufier	17	13	2025-08-20 11:03:35.269895	2025-08-20 11:03:35.269895	f
5654028155	f	t	ARGSENTINEL	14	12	2025-08-20 10:59:27.579132	2025-08-20 10:59:27.579132	f
1017871562	f	t	mid_lyn	\N	17	2025-08-20 12:16:52.940243	2025-08-20 12:16:52.940243	t
1359560791	f	t	jelyfishron	\N	18	2025-08-20 14:14:11.061735	2025-08-20 14:14:11.061735	t
1096920627	f	t	kultyschev10	\N	20	2025-08-20 15:17:13.220997	2025-08-20 15:17:13.220997	f
7717483630	f	f	Krobitik	\N	4	2025-08-14 23:52:36.091653	2025-08-14 23:52:36.091653	f
801700485	f	t	tolstbb	17	8	2025-08-20 10:17:06.0884	2025-08-20 10:17:06.0884	f
2022039753	f	t	Baksik2024	\N	11	2025-08-20 10:51:53.063019	2025-08-20 10:51:53.063019	f
949796701	f	t	wtkitty	\N	7	2025-08-16 21:12:49.055217	2025-08-16 21:12:49.055217	t
810285026	f	t	Ktololp	\N	15	2025-08-20 11:05:13.635526	2025-08-20 11:05:13.635526	t
896475099	f	t	vlxdislxve	\N	14	2025-08-20 11:04:03.85434	2025-08-20 11:04:03.85434	t
7857810365	t	t	underground_vpn_manager_2	\N	21	2025-08-22 11:44:59.6222	2025-08-22 11:44:59.6222	t
8482484435	t	t	underground_vpn_manager_1	\N	22	2025-08-22 14:11:21.785456	2025-08-22 14:11:21.785456	t
\.


--
-- Name: configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.configs_id_seq', 67, true);


--
-- Name: execute_products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.execute_products_id_seq', 3, true);


--
-- Name: finance_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.finance_accounts_id_seq', 22, true);


--
-- Name: moderators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.moderators_id_seq', 2, true);


--
-- Name: payment_receipts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.payment_receipts_id_seq', 3, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.payments_id_seq', 60, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.products_id_seq', 3, true);


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

SELECT pg_catalog.setval('public.subscription_charges_id_seq', 24, true);


--
-- Name: subscriptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.subscriptions_id_seq', 24, true);


--
-- Name: telegram_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.telegram_users_id_seq', 22, true);


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
-- Name: execute_products execute_products_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.execute_products
    ADD CONSTRAINT execute_products_pkey PRIMARY KEY (id);


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
-- Name: subscriptions subscriptions_external_id_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_external_id_key UNIQUE (external_id);


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
-- Name: execute_products execute_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.execute_products
    ADD CONSTRAINT execute_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


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

\unrestrict 11niJaGVjL76rvugDnUa9bcyU5FzhZ5GoflH26AOsxsRa5SKzH98E2TS2TGVkvP

