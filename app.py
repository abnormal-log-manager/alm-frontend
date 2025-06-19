# app.py - URL Management Dashboard for ShortLink API

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json
from datetime import datetime

# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Configuration - Update these to match your API
API_BASE_URL = 'http://alm-api/api'  # Change to your API URL
SHORTURL_ENDPOINT = f'{API_BASE_URL}/ShortUrl'
REDIRECT_ENDPOINT = f'{API_BASE_URL}/r'

# Enums matching the C# backend
TEAMS = ['OPS', 'OMS', 'TMS', 'WMS'] 
LEVELS = ['Warn', 'Error', 'Fatal'] 

class ShortUrlAPI:
    """Helper class to interact with ShortLink API"""
    
    @staticmethod
    def get_all_urls(page=1, page_size=10):
        """Get paginated URLs from the API"""
        try:
            response = requests.get(
                f'{SHORTURL_ENDPOINT}?page={page}&pageSize={page_size}', 
                verify=False
            )  # verify=False for dev only
            if response.status_code == 200:
                data = response.json()
                #print(f"API Response: {data}")  # Debug: Print the full response
                return {
                    'Data': data.get('data', []),
                    'TotalItems': data.get('totalItems', 0),
                    'Page': data.get('page', page),
                    'PageSize': data.get('pageSize', page_size),
                    'TotalPages': data.get('totalPages', 0)
                }
            #print(f"Non-200 status code: {response.status_code}, Response: {response.text}")  # Debug: Non-200 response
            return {'Data': [], 'TotalItems': 0, 'Page': page, 'PageSize': page_size, 'TotalPages': 0}
        except requests.exceptions.RequestException as e:
            print(f"Exception fetching URLs: {e}")
            return {'Data': [], 'TotalItems': 0, 'Page': page, 'PageSize': page_size, 'TotalPages': 0}
    
    @staticmethod
    def create_short_url(original_url, team, level):
        """Create a new shortened URL with team and level"""
        try:
            payload = {
                'originalUrl': original_url,
                'team': team,
                'level': level
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                SHORTURL_ENDPOINT, 
                data=json.dumps(payload), 
                headers=headers,
                verify=False  # verify=False for dev only
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error creating short URL: {e}")
            return None
    
    @staticmethod
    def get_url_by_id(url_id):
        """Get a specific URL by ID"""
        try:
            response = requests.get(f'{SHORTURL_ENDPOINT}/{url_id}', verify=False)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL by ID: {e}")
            return None
    
    @staticmethod
    def delete_url(url_id):
        """Hard delete a URL"""
        try:
            response = requests.delete(f'{SHORTURL_ENDPOINT}/{url_id}', verify=False)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error deleting URL: {e}")
            return False
    
    @staticmethod
    def soft_delete_url(url_id):
        """Soft delete a URL"""
        try:
            response = requests.delete(f'{SHORTURL_ENDPOINT}/softdel?id={url_id}', verify=False)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error soft deleting URL: {e}")
            return False
            
    @staticmethod
    def search_urls(page=1, page_size=10, team=None, level=None, created=None, short_code=None, sort_by=None, descending=False):
        """Search and sort URLs"""
        try:
            params = {
                "page": page,
                "pageSize": page_size,
                "descending": str(descending).lower()
            }
            if team:
                params["team"] = team
            if level:
                params["level"] = level
            if created:
                params["createdDate"] = created
            if short_code:
                params["shortCode"] = short_code
            if sort_by:
                params["sortBy"] = sort_by

            response = requests.get(f'{SHORTURL_ENDPOINT}/search', params=params, verify=False)
            if response.status_code == 200:
                return response.json()
            return {'Data': [], 'TotalItems': 0}
        except requests.exceptions.RequestException as e:
            print(f"Search exception: {e}")
            return {'Data': [], 'TotalItems': 0}
        
    @staticmethod
    def get_team_stats(days=None):
        """Get warning level stats per team, optionally filtered by days"""
        try:
            params = {}
            if days:
                params["days"] = days
            response = requests.get(f"{API_BASE_URL}/stats/per-team", params=params, verify=False)
            if response.status_code == 200:
                return response.json()
            else:
                print("Stats API returned", response.status_code, response.text)
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching team-level stats: {e}")
            return {}


# Route 1: Dashboard - Show all URLs in a table
@app.route('/')
def dashboard():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    team = request.args.get('team')
    level = request.args.get('level')
    created = request.args.get('created')  # expected format: yyyy-mm-dd
    short_code = request.args.get('short_code')
    sort_by = request.args.get('sort_by')
    descending = request.args.get('descending') == 'true'

    data = ShortUrlAPI.search_urls(page, page_size, team, level, created, short_code, sort_by, descending)

    return render_template(
        'dashboard.html',
        urls=data.get('data', []),
        page=data.get('page', page),
        page_size=data.get('pageSize', page_size),
        total_pages=data.get('totalPages', 0),
        total_items=data.get('totalItems', 0),
        selected_team=team,
        selected_level=level,
        selected_created=created,
        selected_sort=sort_by,
        selected_descending=descending
    )

# Route 2: Create new short URL
@app.route('/create', methods=['GET', 'POST'])
def create_url():
    if request.method == 'POST':
        original_url = request.form['original_url'].strip()
        team = request.form['team']
        level = request.form['level']
        
        if not original_url:
            flash('Please enter a valid URL', 'error')
            return render_template('create_url.html', teams=TEAMS, levels=LEVELS)
        
        if team not in TEAMS:
            flash('Please select a valid team', 'error')
            return render_template('create_url.html', teams=TEAMS, levels=LEVELS)
            
        if level not in LEVELS:
            flash('Please select a valid level', 'error')
            return render_template('create_url.html', teams=TEAMS, levels=LEVELS)
        
        # Add http:// if not present
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url
        
        result = ShortUrlAPI.create_short_url(original_url, team, level)
        if result:
            flash(f'Short URL created successfully for {team} team with {level} level!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Failed to create short URL. Please try again.', 'error')
    
    return render_template('create_url.html', teams=TEAMS, levels=LEVELS)

# Route 3: Soft delete URL
@app.route('/soft-delete/<int:url_id>')
def soft_delete_url(url_id):
    if ShortUrlAPI.soft_delete_url(url_id):
        flash('URL soft deleted successfully!', 'success')
    else:
        flash('Failed to soft delete URL.', 'error')
    return redirect(url_for('dashboard'))

# Route 4: Hard delete URL
@app.route('/delete/<int:url_id>')
def delete_url(url_id):
    if ShortUrlAPI.delete_url(url_id):
        flash('URL deleted permanently!', 'success')
    else:
        flash('Failed to delete URL.', 'error')
    return redirect(url_for('dashboard'))

# Route 5: View single URL details
@app.route('/view/<int:url_id>')
def view_url(url_id):
    url_data = ShortUrlAPI.get_url_by_id(url_id)
    if url_data:
        return render_template('view_url.html', url=url_data)
    else:
        flash('URL not found.', 'error')
        return redirect(url_for('dashboard'))

# Route 6: API endpoint to refresh table data (for AJAX)
@app.route('/api/urls')
def api_urls():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    data = ShortUrlAPI.get_all_urls(page, page_size)
    return jsonify(data)

# Route 7: Test redirect functionality
@app.route('/test-redirect/<path:short_code>')
def test_redirect(short_code):
    """Test the redirect functionality of your API"""
    try:
        response = requests.get(f'{REDIRECT_ENDPOINT}/{short_code}', 
                              allow_redirects=False, verify=False)
        if response.status_code in [301, 302]:
            redirect_url = response.headers.get('Location')
            flash(f'Redirect works! Would redirect to: {redirect_url}', 'success')
        else:
            flash('Short code not found or redirect failed.', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Error testing redirect: {e}', 'error')
    
    return redirect(url_for('dashboard'))

# Route 8: Statistics/Info page
@app.route('/stats')
def stats():
    from datetime import datetime, timedelta

    days_filter = request.args.get('days', type=int)
    data = ShortUrlAPI.get_all_urls(page=1, page_size=1000)
    all_urls = data.get('Data', [])

    # Handle possible format issues in createDate
    def parse_date_safe(s):
        try:
            if '.' in s:
                s = s.split('.')[0]
            return datetime.fromisoformat(s)
        except Exception:
            return None

    now = datetime.utcnow()
    if days_filter:
        threshold = now - timedelta(days=days_filter)
    else:
        threshold = None

    filtered_urls = []
    for url in all_urls:
        created_str = url.get('createDate')
        created_at = parse_date_safe(created_str) if created_str else None
        if not created_at:
            continue
        if threshold is None or created_at >= threshold:
            filtered_urls.append(url)

    active_urls = [u for u in filtered_urls if not u.get('isDeleted', False)]
    deleted_urls = [u for u in filtered_urls if u.get('isDeleted', False)]

    stats_data = {
        'total_urls': len(filtered_urls),
        'active_urls': len(active_urls),
        'deleted_urls': len(deleted_urls)
    }

    # Team and level stats for chart
    team_counts = {team: 0 for team in TEAMS}
    level_counts = {level: 0 for level in LEVELS}

    for url in filtered_urls:
        t = url.get('team')
        l = url.get('level')
        if t in team_counts:
            team_counts[t] += 1
        if l in level_counts:
            level_counts[l] += 1

    # For the team-level table
    team_level_stats = ShortUrlAPI.get_team_stats(days=days_filter)
    print("Team level stats:", team_level_stats)

    return render_template(
        'stats.html',
        stats=stats_data,
        urls=filtered_urls[:10],
        team_counts=team_counts,
        level_counts=level_counts,
        team_level_stats=team_level_stats,
        selected_days=days_filter
    )


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

# Template filters
@app.template_filter('truncate_url')
def truncate_url_filter(url, length=50):
    """Truncate long URLs for display"""
    if len(url) <= length:
        return url
    return url[:length] + '...'

from datetime import datetime

@app.template_filter('format_datetime')
def format_datetime_filter(date_string):
    """Format datetime string for display"""
    if not date_string:
        return 'N/A'
    try:
        # Trim to microseconds if needed (Python supports up to 6 digits)
        if '.' in date_string:
            date_part, frac = date_string.split('.')
            frac = frac[:6]  # Keep only first 6 digits
            date_string = f"{date_part}.{frac}"
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%d-%m-%Y %H:%M:%S')
    except:
        return date_string

@app.template_filter('get_level_badge_class')
def get_level_badge_class(level):
    """Get CSS class for level badge"""
    level_classes = {
        'Warn': 'badge-warning',
        'Error': 'badge-danger',
        'Fatal': 'badge-error'
    }
    return level_classes.get(level, 'badge-secondary')

@app.template_filter('get_team_badge_class')
def get_team_badge_class(team):
    """Get CSS class for team badge"""
    team_classes = {
        'OMS': 'badge-primary',
        'WMS': 'badge-info', 
        'TMS': 'badge-detail',
        'OPS': 'badge-secondary'
    }
    return team_classes.get(team, 'badge-secondary')

# Run the application
if __name__ == '__main__':
    # Debug mode shows detailed errors and auto-reloads on code changes
    print("Starting URL Management Dashboard...")
    print(f"API Base URL: {API_BASE_URL}")
    print("Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
