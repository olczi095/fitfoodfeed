from django.test import TestCase
from django.urls import reverse, reverse_lazy
from taggit.models import Tag
from reviews.models import User, Post, Category, Comment


class HomePageTestCase(TestCase):
    def setUp(self):
        self.author1 = User.objects.create(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

        self.post1 = Post.objects.create(
            title='Sample Post Review',
            slug='sample-post-review',
            pub_date = '2020-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post2 = Post.objects.create(
            title='Another Sample Post Review',
            slug='another-post-review',
            pub_date = '2021-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post3 = Post.objects.create(
            title='Again Another Sample Post Review',
            slug='once-more-post-review',
            pub_date = '2021-08-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post4 = Post.objects.create(
            title='The last one',
            slug='the-last-test-post',
            pub_date = '2023-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )

    def test_home_page_returns_correct_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_displays_added_posts(self):
        response = self.client.get('/')
        self.assertContains(response, self.post2.title)
        self.assertContains(response, self.post2.body)

    def test_pagination_displays(self):
        response = self.client.get('/')
        self.assertEqual(response.context['is_paginated'], True)
        self.assertIn('paginator', response.context)

    
class PostDetailTestCase(TestCase):
    def setUp(self):
        self.author1 = User.objects.create(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

        self.post1 = Post.objects.create(
            title='Sample Post Review',
            slug='sample-post-review',
            pub_date = '2020-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )

    def test_post_detail_returns_correct_response(self):
        response = self.client.get(reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_contains_body_and_title(self):
        response = self.client.get(reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}))
        self.assertContains(response, self.post1.body)
        self.assertContains(response, self.post1.title)

    def test_comment_form_displayed(self):
        response = self.client.post(reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)
                                   
    def test_authenticated_user_can_add_comment(self):
        self.client.force_login(self.author1)
        valid_comment_data = {'body': 'This is a random comment written by an authenticated user.'}
        response = self.client.post(
            reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}),
            data=valid_comment_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_fields_added_correctly_for_authenticated_user(self):
        self.client.force_login(self.author1)
        valid_comment_data = {'body': 'This is a random comment written by an authenticated user.'}
        self.client.post(reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}), data=valid_comment_data)
        new_comment = Comment.objects.last()

        self.assertEqual(new_comment.post, self.post1)
        self.assertFalse(new_comment.active)
        self.assertIsNone(new_comment.unlogged_user)
        self.assertEqual(new_comment.logged_user, self.author1)

    def test_unauthenticated_user_can_add_comment(self):
        self.client.logout()
        valid_comment_data = {'body': 'This is a random comment written by an unauthenticated user.'}
        response = self.client.post(
            reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}),
            data=valid_comment_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_fields_added_correctly_for_unauthenticated_user(self):
        valid_comment_data = {'body': 'This is a random comment written by an authenticated user.'}
        self.client.post(reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}),data=valid_comment_data)
        new_comment = Comment.objects.last()
        
        self.assertEqual(new_comment.post, self.post1)
        self.assertFalse(new_comment.active)
        self.assertIsNone(new_comment.logged_user)
        self.assertEqual(new_comment.unlogged_user, 'guest')

    def test_display_success_message_after_comment_addition(self):
        valid_comment_data = {'body': 'This is a random comment written by an authenticated user.'}
        response = self.client.post(
            reverse('app_reviews:detail_review', kwargs={'slug': self.post1.slug}),
                    data=valid_comment_data,
                    follow=True
            )
        expected_success_message_excerpt = 'comment successfully submitted'
        messages = [str(message).lower() for message in response.context['messages']]
        self.assertTrue(any(expected_success_message_excerpt in message for message in messages))


class PostCreateTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

    def test_unlogged_user_redirect_to_login(self):
        response = self.client.get(reverse('app_reviews:create_review'))
        self.assertEqual(response.status_code, 302)  
        expected_url = reverse('app_accounts:login') + '?next=' + reverse('app_reviews:create_review')
        self.assertRedirects(response, expected_url)

    
    def test_logged_user_without_permission_returns_403_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse_lazy('app_reviews:create_review'))
        self.assertEqual(response.status_code, 403)


class PostCreateWithPermissionTestCase(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_superuser(
            username='admin',
            password='admin-password'
        )
        self.client.force_login(self.adminuser)

    def test_display_add_review_success(self):
        self.assertTrue(self.adminuser.has_perm('reviews.add_post'))
        response = self.client.get(reverse_lazy('app_reviews:create_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_create.html')

    def test_successful_post_creation_redirect(self):
        new_review = {
            'title': 'New Review',
            'body': 'The body of the new review',
            'status': 'PUB'
        }
        response = self.client.post(reverse_lazy('app_reviews:create_review'), data=new_review)
        expected_url_after_post = '/new-review/'  #slug created automatically based on 'New Review'
        self.assertRedirects(response, expected_url_after_post)

    def test_successful_post_adding_to_database(self):
        first_review = {
            'title': 'New Review',
            'body': 'The body of the new review',
            'status': 'PUB'
        }
        second_review = {
            'title': 'Second Review',
            'body': 'The body of the new review',
            'status': 'PUB'

        }
        self.client.post(reverse_lazy('app_reviews:create_review'), data=first_review)
        self.client.post(reverse_lazy('app_reviews:create_review'), data=second_review)

        posts_amount = len(Post.objects.all())
        self.assertEqual(posts_amount, 2)

        # Check if the author is assigned to the posts
        first_post = Post.objects.get(title='New Review')
        author_of_first_post = first_post.author
        self.assertEqual(author_of_first_post, self.adminuser)


class PostUpdateTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author', 
            password='xyz', 
            is_author=True
        )
        self.category = Category.objects.create(
            name='Peanut Butter'
        )
        self.review = Post.objects.create(
            title='Protein Bar Review',
            body='This is a review of Protein Bar. I really liked it.',
            author=self.author,
            category=self.category,
        )

    def test_author_can_access_update_view(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('app_reviews:update_review', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_update.html')

    def test_superuser_can_access_update_view(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='pass'
        )
        self.client.force_login(self.author)
        response = self.client.get(reverse('app_reviews:update_review', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_update.html')

    def test_staff_can_access_update_view(self):
        self.staff = User.objects.create_user(
            username='staff',
            password='abc',
            is_staff=True
        )
        self.client.force_login(self.author)
        response = self.client.get(reverse('app_reviews:update_review', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_update.html')

    def test_normal_user_cannot_access_update_view(self):
        self.normal_user = User.objects.create_user(
            username='normal_user',
            password='abc',
        )
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('app_reviews:update_review', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_other_author_cannot_update_post(self):
        self.second_author = User.objects.create_user(
            username='second_author',
            password='xyz',
            is_author=True
        )
        self.client.force_login(self.second_author)
        response = self.client.get(reverse('app_reviews:update_review', kwargs={'pk': self.review.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
    
    def test_not_logged_user_redirect_login_page(self):
        self.client.logout()
        response = self.client.get(reverse('app_reviews:update_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')


class PostDeleteTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author', 
            password='xyz', 
            is_author=True
        )
        self.review = Post.objects.create(
            title='Vegan Chocolate Review',
            body='This is a review of Vegan Chocolate. Not tasty.',
            author=self.author,
        )
    
    def test_author_can_access_delete_view(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('app_reviews:delete_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('reviews/review_delete.html')

    def test_staff_can_access_delete_view(self):
        User.objects.create_user(
            username='admin',
            password='abc',
            is_staff=True
        )
        self.client.force_login(self.author)
        response = self.client.get(reverse('app_reviews:delete_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('reviews/review_delete.html')

    def test_superuser_can_access_delete_view(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            password='abc'
        )
        self.client.force_login(superuser)
        response = self.client.get(reverse('app_reviews:delete_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('reviews/review_delete.html')

    def test_other_author_cannot_delete_post(self):
        other_author = User.objects.create_user(
            username='other_author',
            password='xyz',
            is_author=True
        )
        self.client.force_login(other_author)
        response = self.client.get(reverse('app_reviews:delete_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_random_user_redirect_login_page(self):
        self.client.logout()
        response = self.client.get(reverse('app_reviews:delete_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_get_success_message(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('app_reviews:delete_review', kwargs={'pk': self.review.pk}), follow=True)
        self.assertTemplateUsed(response, 'reviews/home.html')

        success_messages = [str(message) for message in response.context['messages']]
        expected_message = f"Post <strong>{self.review.title}</strong> deleted successfully."
        self.assertEqual(success_messages[0], expected_message)


class PostStatusTestCase(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_superuser(
            username='author',
            password='author-password'
        )
        self.client.force_login(self.adminuser)

    def test_post_published_should_appear_on_homepage(self):
        self.post = Post.objects.create(
            title='The new review',
            body='This is the body of the new review.',
            status='PUB'
        )
        homepage = self.client.get(reverse('app_reviews:home'))
        self.assertContains(homepage, self.post)

    def test_post_to_publish_should_not_appear_on_homepage(self):
        self.post = Post.objects.create(
            title='The first to-publish review',
            body='This is the body of a two-publish review.',
            status='TO_PUB'
        )
        homepage = self.client.get(reverse('app_reviews:home'))
        self.assertNotContains(homepage, self.post)

    def test_post_to_publish_should_not_be_published(self):
        data = {
            'title': 'The second to-publish review',
            'body': 'This is the body of a second two-publish review.',
            'status': 'TO_PUB',
            'slug': 'the-second-to-publish-review'
        }
        response = self.client.post(reverse('app_reviews:create_review'), data)
        self.assertRedirects(response, '/') # Redirect to the homepage, not to the post_detail
        response = self.client.get(reverse('app_reviews:detail_review', kwargs={'slug': data['slug']}))
        self.assertEqual(response.status_code, 404)

    def test_post_to_publish_create_and_save(self):
        data = {
            'title': 'The third to-publish review',
            'body': 'This is the body of a second two-publish review.',
            'status': 'TO_PUB',
        }
        self.client.post(reverse('app_reviews:create_review'), data)

        post_amount = Post.objects.count()
        self.assertEqual(post_amount, 1)


    def test_post_draft_should_not_appear_on_homepage(self):
        self.post = Post.objects.create(
            title='The first draft review',
            body='This is the body of a draft review.',
            status='DRAFT'
        )
        homepage = self.client.get(reverse('app_reviews:home'))
        self.assertNotContains(homepage, self.post)

    def test_post_draft_should_not_be_published(self):
        data = {
            'title': 'The second draft review',
            'body': 'This is the body of a second draft review.',
            'status': 'DRAFT',
            'slug': 'the-second-draft-review'
        }
        response = self.client.post(reverse('app_reviews:create_review'), data)
        self.assertRedirects(response, '/') # Redirect to the homepage, not to the post_detail
        response = self.client.get(reverse('app_reviews:detail_review', kwargs={'slug': data['slug']}))
        self.assertEqual(response.status_code, 404)

    def test_post_draft_create_and_save(self):
        data = {
            'title': 'The third draft review',
            'body': 'This is the body of a third draft review.',
            'status': 'DRAFT',
        }
        self.client.post(reverse('app_reviews:create_review'), data)

        post_amount = Post.objects.count()
        self.assertEqual(post_amount, 1)

    def test_popular_posts_in_context(self):
        response = self.client.get(reverse('app_reviews:home'))
        self.assertIn('popular_posts', response.context)
        self.assertIsInstance(response.context['popular_posts'], list)
        self.assertLessEqual(len(response.context['popular_posts']), 5)
        self.assertGreaterEqual(len(response.context['popular_posts']), 0)

    def test_recent_comments_in_context(self):
        response = self.client.get(reverse('app_reviews:home'))
        self.assertIn('recent_comments', response.context)
        self.assertIsInstance(response.context['recent_comments'], list)
        self.assertLessEqual(len(response.context['recent_comments']), 3)
        self.assertGreaterEqual(len(response.context['recent_comments']), 0)


class TagsListTestCase(TestCase):
    def test_successful_tags_list_displaying(self):
        response = self.client.get(reverse('app_reviews:tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/tags.html')

    
class TaggedPostsListTestCase(TestCase):
    def setUp(self):
        self.tag_bars = Tag.objects.create(
            name='bars'
        )
        self.tag_drinks = Tag.objects.create(
            name='drinks'
        )
        self.post1 = Post.objects.create(
            title='Chocolate bar',
            body='This is the body of the chocolate bar review.',
            status='PUB',
        )
        self.post2 = Post.objects.create(
            title='Protein bar',
            body='This is the body of the protein bar review.',
            status='TO_PUB',
        )
        self.post3 = Post.objects.create(
            title='White chocolate bar',
            body='This is the body of the white chocolate bar review.',
            status='DRAFT',
        )
        self.post4 = Post.objects.create(
            title='Energydrink Zero',
            body='This is the body of the Energydrink Zero',
            status='PUB',
        )
        self.post5 = Post.objects.create(
            title='Fruit Bar',
            body='This is the body of the Fruit Zero',
            status='PUB',
        )

        posts = [self.post1, self.post2, self.post3, self.post5]
        for post in posts:
            post.tags.add(self.tag_bars)
        self.post4.tags.add(self.tag_drinks)

    def test_tag_page_success(self):
        tag_name = self.tag_bars.name
        response = self.client.get(reverse('app_reviews:tag', kwargs={'tag_name': tag_name}))
        self.assertEqual(response.status_code, 200)
    
    def test_tag_page_uses_home_template(self):
        tag_name = self.tag_bars.name
        self.client.get(reverse('app_reviews:tag', kwargs={'tag_name': tag_name}))
        self.assertTemplateUsed('reviews/home.html')

    def test_filtering_tagged_posts(self):
        tag_name = self.tag_bars.name

        response = self.client.get(reverse('app_reviews:tag', kwargs={'tag_name': tag_name}))
        filtered_tagged_posts = [self.post1, self.post5] # Posts with PUB status and BARS tag

        self.assertQuerysetEqual(
            response.context['posts'],
            filtered_tagged_posts
        )

    
class CategoryViewsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='masła orzechowe'
        )        
        self.post1 = Post.objects.create(
            title='Chocolate bar',
            body='This is the body of the chocolate bar review.',
            status='PUB',
        )
        self.post2 = Post.objects.create(
            title='Peanut Butter Crunchy',
            category=self.category,
            body='This is the body of the peanut butter crunchy review.',
            status='PUB',
        )
        self.post3 = Post.objects.create(
            title='Peanut Butter with white chocolate',
            category=self.category,
            body='This is the body of the peanut butter with white chocolate review.',
            status='DRAFT',
        )

    def test_successfull_category_page_load(self):
        response = self.client.get(reverse('app_reviews:category', kwargs={'category_name': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/home.html')

    def test_display_published_post_from_proper_category(self):
        category_peanut_butter = self.category.slug
        response = self.client.get(reverse('app_reviews:category', kwargs={'category_name': category_peanut_butter}))
        
        expected_posts = [self.post2]
        self.assertQuerysetEqual(
            response.context['posts'],
            expected_posts
        )