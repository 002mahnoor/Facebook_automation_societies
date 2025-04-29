
def profile():
    global pfp_view
    global prof_link
    global bio
    global deliver
    global view
    global profile_manager
    global msg_send, page_user
    actions = ActionChains(driver)
    
    try:
        # Extract the total number of iterations from the given XPath
        total_iterations_xpath = "(//*[contains(@class, 'html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs')])[1]"
        element = driver.find_element(By.XPATH, total_iterations_xpath)
        total_iterations_text = element.text.strip()
        print("Total posts that are to be checked:" + total_iterations_text)
        
        try:
            total_iterations = int(total_iterations_text)
            print(f"Total iterations to process: {total_iterations}")
        except ValueError:
            print(f"Failed to convert text '{total_iterations_text}' to an integer. Defaulting to 1.")
            total_iterations = 1
        
        # Iterate for the number of posts specified
        scroll_timer(5)
        print('hello1')
        row = 0
        col = 0
        attempt = 0
        
        while attempt < total_iterations:
            attempt += 1
            print(f"Iteration {attempt} of {total_iterations}")
            
            time.sleep(random.uniform(2, 4))
            page_user = get_username()
            print("profile is running")
            
            path = f"(//*[contains(@class, 'x1lliihq') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'x4gyw5p') and contains(@class, 'x1ntc13c') and contains(@class, 'x9i3mqj') and contains(@class, 'x11i5rnm') and contains(@class, 'x2pgyrj')])[{col + 1}]"
            print('path alot')
            print(path)
            
            posts = driver.find_elements(By.XPATH, path)
            print('length: ', len(posts))
            time.sleep(random.uniform(5, 8))
            
            for post in posts:
                try:
                    print('element giving')
                    post.click()
                    print('click giving')
                    time.sleep(random.uniform(5, 8))
                    
                    like = driver.find_elements(By.XPATH, "//span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")
                    like = like[-1]
                    try:
                        a_tag = like.find_element(By.XPATH, '..')  # Navigate to parent
                        href_value = a_tag.get_attribute('href')
                        print(f'get url: {href_value}')
                        store(href_value)
                    except Exception as e:
                        print('Error in get parent tag........')

                    time.sleep(random.uniform(5, 10))
                    driver.back()
                    print('back giving')
                    time.sleep(random.uniform(5, 10))
                    col += 1
                except Exception as e:
                    print(f"Error processing post: {e}")
            time.sleep(5)
        print('Profile Done...')
    except Exception as e:
        print(f'Profile Error...{e}') 
