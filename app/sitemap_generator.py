import os


def build_sitemap(template_dir):
    sitemap = []
    for subdir, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                # Assuming the directory name is part of the URL path
                subdir_path = subdir.replace(template_dir, '').lstrip(os.sep)
                sitemap.append((subdir_path, file))
    return sitemap


def print_sitemap(sitemap):
    for path, filename in sitemap:
        url = f'/{path}/{filename}' if path else f'/{filename}'
        print(f'<li><a href="{url}">{filename}</a></li>')


def main():
    # Replace with your actual templates directory path
    template_dir = 'app\\templates'
    sitemap = build_sitemap(template_dir)
    print_sitemap(sitemap)
    print(f'Total pages: {len(sitemap)}')


if __name__ == "__main__":
    main()
