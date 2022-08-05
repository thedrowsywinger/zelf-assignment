# Zelf Assessment

Project Setup:

```sh
python -m source venv env_zelf_assignment
source env_zelf_assignment/bin/activate
cd zelf-assignment
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Sample Requests:

## Scrape Images from Ebay

Sample URLs:

1. https://www.ebay.com/b/Samsung/bn_21834655
2. https://www.ebay.com/b/Apple/bn_21819543

Sample POST request:
URL: 127.0.0.1:8000/api/core/scrape-ebay/

```sh
{
    "url": "https://www.ebay.com/b/Samsung/bn_21834655"
}
```

Sample Response:

```sh
{
    "message": "Success",
    "Invalid URLs": []
}
```

## Query Images

URL: 127.0.0.1:8000/api/core/image/

#### Sample GET request:

### Filter: Small Image Size

```sh
{
    "id": 55,
    "size": "small"
}
```

Sample Response:

```sh
{
    "message": "Success",
    "data": {
        "id": 55,
        "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908.jpg",
        "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
        "meta_data": {
            "original_url": "https://i.ebayimg.com/thumbs/images/g/HtcAAOSwT6lePUom/s-l225.jpg",
            "scrape_date": "2022-08-05",
            "height": 170,
            "width": 170
        },
        "resized_image": {
            "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908_SMALL.jpg",
            "meta_data": {
                "width": 256,
                "height": 256
            }
        }
    }
}
```

### Filter: Medium Image Size

```sh
{
    "id": 55,
    "size": "medium"
}
```

Sample Response:

```sh
{
    "message": "Success",
    "data": {
        "id": 55,
        "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908.jpg",
        "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
        "meta_data": {
            "original_url": "https://i.ebayimg.com/thumbs/images/g/HtcAAOSwT6lePUom/s-l225.jpg",
            "scrape_date": "2022-08-05",
            "height": 170,
            "width": 170
        },
        "resized_image": {
            "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908_MEDIUM.jpg",
            "meta_data": {
                "width": 256,
                "height": 256
            }
        }
    }
}
```

### Filter: Large Image Size

```sh
{
    "id": 55,
    "size": "large"
}
```

Sample Response:

```sh
{
    "message": "Success",
    "data": {
        "id": 55,
        "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908.jpg",
        "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
        "meta_data": {
            "original_url": "https://i.ebayimg.com/thumbs/images/g/HtcAAOSwT6lePUom/s-l225.jpg",
            "scrape_date": "2022-08-05",
            "height": 170,
            "width": 170
        },
        "resized_image": {
            "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908_LARGE.jpg",
            "meta_data": {
                "width": 256,
                "height": 256
            }
        }
    }
}
```

### Filter: Id

```sh
{
    "id": 55
}
```

Sample Response:

```sh
{
    "message": "Success",
    "data": {
        "id": 55,
        "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908.jpg",
        "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
        "meta_data": {
            "original_url": "https://i.ebayimg.com/thumbs/images/g/HtcAAOSwT6lePUom/s-l225.jpg",
            "scrape_date": "2022-08-05",
            "height": 170,
            "width": 170
        }
    }
}
```

### Filter: Original URL

```sh
{
    "original_url": "https://www.ebay.com/b/Apple/bn_21819543"
}
```

Sample Response:

```sh
{
    "message": "Success",
    "count": 10,
    "data": [
        {
            "id": 55,
            "image_path": "/media/67445ad1-da5f-41cf-9e18-4a0462395908.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/HtcAAOSwT6lePUom/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 56,
            "image_path": "/media/8838168f-25fa-4adc-a80b-1a13293ab30d.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/xqwAAOSwNThePUoq/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 57,
            "image_path": "/media/0debc3d4-b26a-464c-8b1b-af2dfbdb6152.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/ZvoAAOSwePpePUot/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 58,
            "image_path": "/media/7202e5a4-b625-42ea-91a2-53772ea90232.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/SGYAAOSwwJ1ePUox/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 59,
            "image_path": "/media/31a05d05-97bf-4e3d-8f0d-21374aeaba2b.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/bzgAAOSwM4hePUo1/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 60,
            "image_path": "/media/91b26178-531f-401c-947e-9fb8790eb38e.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/jVkAAOSwxH1ePUpn/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 61,
            "image_path": "/media/3b01c173-aa3d-443f-80c5-1c4b7a90d1d9.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/I84AAOSwq1lePUpr/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 62,
            "image_path": "/media/fb2f8fb6-2f4f-4603-8740-0c0d115e2644.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/s2AAAOSwqzFePUpv/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 63,
            "image_path": "/media/5ae57c69-c246-41d9-8539-7353b84130f3.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/5aQAAOSwTWhePUpy/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        },
        {
            "id": 64,
            "image_path": "/media/da991a0d-af67-47d9-bd00-dc4e71056d3e.jpg",
            "original_url": "https://www.ebay.com/b/Apple/bn_21819543",
            "meta_data": {
                "original_url": "https://i.ebayimg.com/thumbs/images/g/v-QAAOSwzWFePUp1/s-l225.jpg",
                "scrape_date": "2022-08-05",
                "height": 170,
                "width": 170
            }
        }
    ]
}
```
