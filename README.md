# dot
Social media application built using Python, FastAPI, JavaScript, HTML/TailwindCSS, and PostgreSQL.

## Background
Dot was created to address the overwhelming negativity that dominates much of modern social media. In contrast to platforms filled with outrage, toxicity, and algorithm-driven noise, Dot offers a quiet, kind space focused entirely on positivity. It's a place to share uplifting moments - a song stuck in your head, a small win, or just something that made you smile - with no algorithms, no trolls, and no drama. Dot aims to bring back a sense of connection, empathy, and joy to the online experience.

## Screenshots
<details>

<summary>Click me!</summary>

### Landing Page
![Screenshot of landing page](demo/landing-page.png "Landing Page")

### Feed
![Screenshot of feed page](demo/feed.png "Feed Page")

### User Profile
![Screenshot of user profile page](demo/user-profile.png "User Profile Page")

### Dashboard (zoomed out slightly for clarity)
![Screenshot of dashboard page](demo/dashboard.png "Dashboard Page")

</details>

## Installation
### Clone the repository
Clone the Dot repository by running:
```bash
git clone https://github.com/hmont/dot
```

### Install dependencies with Poetry
First, install Poetry itself:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then, install the project dependencies:
```bash
# make sure you're in the project root directory!
cd dot

poetry install --no-root
```

### Install sentiment analysis model
As per Dot's stated purpose of preventing toxicity on social media, Dot includes functionality wherein any text a user attempts to post is processed using a sentiment analysis NLP model. Content that is determined to be too negative will not be posted.

Due to file size and copyright limitations, no sentiment analysis model is included in this repository. Instead, it is recommended to download a pretrained/fine-tuned sentiment analysis model from e.g. [Hugging Face](https://huggingface.co/). After download, the model and its associated JSON files will need to be placed into a directory called `model`. This may also require modifying the [classifier code](https://github.com/hmont/dot/blob/main/adapters/classifier.py) to better suit the different model.

### Setup PostgreSQL database
#### Note: The included `db.sql` schema file has not been extensively tested. If you run into any issues, try creating the tables manually using the SQLAlchemy models as a guide.

Import the database structure:

```bash
# make sure you're in the project root directory!
cd dot

psql -U <YOUR_USERNAME> -d <YOUR_DATABASE> -f ext/db.sql
```


### Setup NGINX reverse proxy (for production environments)
Dot does not natively use HTTPS/SSL as part of the application itself. As such, in production, it is highly recommended to use Dot behind a reverse proxy which allows for HTTPS (NGINX in this example).

#### Get an SSL certificate
In order to use HTTPS, you will first need an SSL certificate for your domain. How exactly to obtain one is unfortunately beyond the scope of this guide, however a popular (and free) choice is Let's Encrypt via [Certbot](https://certbot.eff.org/).

#### Edit NGINX config
First, copy the example NGINX config to the project directory:
```bash
# make sure you're in the project root directory!
cd dot

cp ext/nginx.example nginx.conf
```
You can then modify the configuration as needed. Exactly which configuration you use will ultimately depend on your setup and needs, but generally, all you need to modify is the `server_name` (to reflect your domain), as well as the `ssl_certificate` and `ssl_certificate_key` to reflect the location of your SSL certificate and key.

After editing the configuration, create a link in `sites-enabled`:
```bash
sudo ln nginx.conf /etc/nginx/sites-enabled/dot
```
Finally, test the configuration, and, assuming no errors, reload NGINX:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Configure Dot settings
Dot itself requires a PostgreSQL database as well as Redis.

To configure access to these (or other options such as the host/port Dot runs on), first copy the example .env file to the project root directory:
```bash
# make sure you're in the project root directory!
cd dot

cp ext/.env.example .env
```

Then modify the configuration as needed.
