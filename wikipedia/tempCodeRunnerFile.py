summary = wiki_summary(name)
            try:
                if len(summary) > 1300:
                    summary = summary[:1300]
                    last_period = summary.rfind('.')
                    summary = summary[:last_period+1]
                update_data = summary
                create_content(page_id, update_data)
            except:
                pass