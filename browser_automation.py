#!/usr/bin/env python3
"""
DataScope Enhanced - Browser Automation Module
Handles data collection from sites requiring JavaScript execution or user login
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BrowserAutomation:
    """Browser automation for complex data collection scenarios"""
    
    def __init__(self, headless: bool = True, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.headless = headless
        self.driver = None
        
        # Platform-specific configurations
        self.platform_configs = {
            'lemon8': {
                'login_url': 'https://www.lemon8-app.com/login',
                'selectors': {
                    'login_button': '[data-testid="login-button"]',
                    'username_field': 'input[type="email"]',
                    'password_field': 'input[type="password"]',
                    'posts': '[data-testid="post-item"]',
                    'post_content': '.post-content',
                    'post_author': '.author-name',
                    'post_engagement': '.engagement-stats',
                    'load_more': '[data-testid="load-more"]'
                },
                'wait_time': 3,
                'scroll_pause': 2
            },
            'instagram': {
                'login_url': 'https://www.instagram.com/accounts/login/',
                'selectors': {
                    'username_field': 'input[name="username"]',
                    'password_field': 'input[name="password"]',
                    'login_button': 'button[type="submit"]',
                    'posts': 'article',
                    'post_content': '[data-testid="post-content"]'
                },
                'wait_time': 5,
                'scroll_pause': 3
            },
            'linkedin': {
                'login_url': 'https://www.linkedin.com/login',
                'selectors': {
                    'username_field': '#username',
                    'password_field': '#password',
                    'login_button': 'button[type="submit"]',
                    'posts': '.feed-shared-update-v2',
                    'post_content': '.feed-shared-text'
                },
                'wait_time': 5,
                'scroll_pause': 2
            }
        }
    
    def setup_driver(self) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Disable images and CSS for faster loading (optional)
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def login_to_platform(self, platform: str, credentials: Dict[str, str]) -> bool:
        """Login to a specific platform using stored credentials"""
        
        if platform not in self.platform_configs:
            self.logger.error(f"Platform {platform} not supported")
            return False
        
        config = self.platform_configs[platform]
        
        try:
            if not self.driver:
                self.setup_driver()
            
            # Navigate to login page
            self.driver.get(config['login_url'])
            wait = WebDriverWait(self.driver, 10)
            
            # Wait for and fill username
            username_field = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, config['selectors']['username_field']))
            )
            username_field.clear()
            username_field.send_keys(credentials['username'])
            
            # Fill password
            password_field = self.driver.find_element(By.CSS_SELECTOR, config['selectors']['password_field'])
            password_field.clear()
            password_field.send_keys(credentials['password'])
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, config['selectors']['login_button'])
            login_button.click()
            
            # Wait for login to complete
            time.sleep(config['wait_time'])
            
            # Check if login was successful (platform-specific logic)
            if self._verify_login_success(platform):
                self.logger.info(f"Successfully logged into {platform}")
                return True
            else:
                self.logger.error(f"Login to {platform} failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login to {platform}: {str(e)}")
            return False
    
    def _verify_login_success(self, platform: str) -> bool:
        """Verify that login was successful"""
        try:
            # Check if we're redirected away from login page
            current_url = self.driver.current_url
            login_url = self.platform_configs[platform]['login_url']
            
            # Simple check: if we're not on the login page anymore, assume success
            return login_url not in current_url
            
        except Exception:
            return False
    
    def collect_platform_data(self, platform: str, collection_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect data from a specific platform"""
        
        if platform not in self.platform_configs:
            self.logger.error(f"Platform {platform} not supported")
            return []
        
        config = self.platform_configs[platform]
        collected_data = []
        
        try:
            # Navigate to the target page
            target_url = collection_params.get('url', f"https://www.{platform}.com")
            self.driver.get(target_url)
            
            # Wait for content to load
            time.sleep(config['wait_time'])
            
            # Scroll and collect data
            max_scrolls = collection_params.get('max_scrolls', 5)
            items_collected = 0
            max_items = collection_params.get('max_items', 50)
            
            for scroll_count in range(max_scrolls):
                # Find posts/items on the page
                posts = self.driver.find_elements(By.CSS_SELECTOR, config['selectors']['posts'])
                
                for post in posts[items_collected:]:
                    if items_collected >= max_items:
                        break
                    
                    post_data = self._extract_post_data(post, config['selectors'], platform)
                    if post_data:
                        collected_data.append(post_data)
                        items_collected += 1
                
                if items_collected >= max_items:
                    break
                
                # Scroll down to load more content
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(config['scroll_pause'])
                
                # Check if there's a "Load More" button
                try:
                    load_more_button = self.driver.find_element(By.CSS_SELECTOR, config['selectors'].get('load_more', ''))
                    if load_more_button.is_displayed():
                        load_more_button.click()
                        time.sleep(config['wait_time'])
                except NoSuchElementException:
                    pass
            
            self.logger.info(f"Collected {len(collected_data)} items from {platform}")
            return collected_data
            
        except Exception as e:
            self.logger.error(f"Error collecting data from {platform}: {str(e)}")
            return collected_data
    
    def _extract_post_data(self, post_element, selectors: Dict[str, str], platform: str) -> Optional[Dict[str, Any]]:
        """Extract data from a single post element"""
        
        try:
            post_data = {
                'platform': platform,
                'collected_at': time.time(),
                'url': self.driver.current_url
            }
            
            # Extract content
            if 'post_content' in selectors:
                try:
                    content_element = post_element.find_element(By.CSS_SELECTOR, selectors['post_content'])
                    post_data['content'] = content_element.text.strip()
                except NoSuchElementException:
                    post_data['content'] = post_element.text.strip()
            
            # Extract author
            if 'post_author' in selectors:
                try:
                    author_element = post_element.find_element(By.CSS_SELECTOR, selectors['post_author'])
                    post_data['author'] = author_element.text.strip()
                except NoSuchElementException:
                    post_data['author'] = 'Unknown'
            
            # Extract engagement metrics
            if 'post_engagement' in selectors:
                try:
                    engagement_element = post_element.find_element(By.CSS_SELECTOR, selectors['post_engagement'])
                    post_data['engagement'] = engagement_element.text.strip()
                except NoSuchElementException:
                    post_data['engagement'] = '0'
            
            # Extract any links
            try:
                links = post_element.find_elements(By.TAG_NAME, 'a')
                post_data['links'] = [link.get_attribute('href') for link in links if link.get_attribute('href')]
            except:
                post_data['links'] = []
            
            # Extract images
            try:
                images = post_element.find_elements(By.TAG_NAME, 'img')
                post_data['images'] = [img.get_attribute('src') for img in images if img.get_attribute('src')]
            except:
                post_data['images'] = []
            
            return post_data if post_data.get('content') else None
            
        except Exception as e:
            self.logger.error(f"Error extracting post data: {str(e)}")
            return None
    
    def search_platform(self, platform: str, search_query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Search for specific content on a platform"""
        
        search_urls = {
            'lemon8': f"https://www.lemon8-app.com/search?q={search_query}",
            'instagram': f"https://www.instagram.com/explore/tags/{search_query.replace(' ', '')}",
            'linkedin': f"https://www.linkedin.com/search/results/content/?keywords={search_query}"
        }
        
        if platform not in search_urls:
            self.logger.error(f"Search not supported for platform: {platform}")
            return []
        
        collection_params = {
            'url': search_urls[platform],
            'max_items': max_results,
            'max_scrolls': 3
        }
        
        return self.collect_platform_data(platform, collection_params)
    
    def save_session_data(self, platform: str, data: List[Dict[str, Any]]) -> str:
        """Save collected data to cache"""
        
        timestamp = int(time.time())
        filename = f"{platform}_session_{timestamp}.json"
        filepath = self.cache_dir / filename
        
        session_data = {
            'platform': platform,
            'timestamp': timestamp,
            'data_count': len(data),
            'data': data
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        self.logger.info(f"Session data saved to: {filepath}")
        return str(filepath)
    
    def close(self):
        """Clean up browser resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None

class BrowserDataCollector:
    """High-level interface for browser-based data collection"""
    
    def __init__(self, headless: bool = True):
        self.automation = BrowserAutomation(headless=headless)
        self.logger = logging.getLogger(__name__)
    
    def collect_with_login(self, platform: str, credentials: Dict[str, str], 
                          collection_params: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data from a platform requiring login"""
        
        results = {
            'platform': platform,
            'success': False,
            'data': [],
            'error': None
        }
        
        try:
            # Setup browser
            self.automation.setup_driver()
            
            # Login
            if self.automation.login_to_platform(platform, credentials):
                # Collect data
                data = self.automation.collect_platform_data(platform, collection_params)
                
                results['success'] = True
                results['data'] = data
                results['data_count'] = len(data)
                
                # Save session data
                cache_file = self.automation.save_session_data(platform, data)
                results['cache_file'] = cache_file
            else:
                results['error'] = f"Failed to login to {platform}"
                
        except Exception as e:
            results['error'] = str(e)
            self.logger.error(f"Collection error: {str(e)}")
        
        finally:
            self.automation.close()
        
        return results
    
    def collect_public_data(self, platform: str, collection_params: Dict[str, Any]) -> Dict[str, Any]:
        """Collect publicly available data (no login required)"""
        
        results = {
            'platform': platform,
            'success': False,
            'data': [],
            'error': None
        }
        
        try:
            # Setup browser
            self.automation.setup_driver()
            
            # Collect data
            data = self.automation.collect_platform_data(platform, collection_params)
            
            results['success'] = True
            results['data'] = data
            results['data_count'] = len(data)
            
            # Save session data
            cache_file = self.automation.save_session_data(platform, data)
            results['cache_file'] = cache_file
                
        except Exception as e:
            results['error'] = str(e)
            self.logger.error(f"Collection error: {str(e)}")
        
        finally:
            self.automation.close()
        
        return results

def main():
    """Test browser automation"""
    logging.basicConfig(level=logging.INFO)
    
    collector = BrowserDataCollector(headless=False)  # Set to False to see browser
    
    # Test public data collection
    collection_params = {
        'url': 'https://www.lemon8-app.com',
        'max_items': 10,
        'max_scrolls': 2
    }
    
    results = collector.collect_public_data('lemon8', collection_params)
    print(f"Collected {results.get('data_count', 0)} items")
    print(f"Success: {results['success']}")
    if results.get('error'):
        print(f"Error: {results['error']}")

if __name__ == "__main__":
    main()

