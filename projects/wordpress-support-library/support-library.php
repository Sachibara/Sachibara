<?php
/**
 * Plugin Name: Sachibara Support Library
 * Description: Searchable technical knowledge base with topic taxonomy and a responsive shortcode directory.
 * Version: 1.0.0
 * Author: Jim Rodmark Camus
 * License: MIT
 * Requires PHP: 8.1
 */
if(!defined('ABSPATH'))exit;
function sachibara_kb_register():void {
    register_post_type('sachi_article',['labels'=>['name'=>'Support Articles','singular_name'=>'Support Article'], 'public'=>true, 'show_in_rest'=>true,
        'has_archive'=>true,'rewrite'=>['slug'=>'support-library'],'supports'=>['title','editor','excerpt','revisions'],'menu_icon'=>'dashicons-sos']);
    register_taxonomy('sachi_topic','sachi_article',['label'=>'Support Topics','public'=>true,'hierarchical'=>true,'show_in_rest'=>true,'rewrite'=>['slug'=>'support-topic']]);
}
add_action('init','sachibara_kb_register');
register_activation_hook(__FILE__,function(){sachibara_kb_register();flush_rewrite_rules();});
register_deactivation_hook(__FILE__,function(){flush_rewrite_rules();});
add_action('wp_enqueue_scripts',function(){wp_register_style('sachibara-kb',plugins_url('assets/library.css',__FILE__),[], '1.0.0');wp_enqueue_style('sachibara-kb');});
add_shortcode('support_library',function():string {
    $query=isset($_GET['kb_search'])&&is_string($_GET['kb_search'])?sanitize_text_field(wp_unslash($_GET['kb_search'])):'';
    $topic=isset($_GET['kb_topic'])?absint($_GET['kb_topic']):0;
    $page=max(1,isset($_GET['kb_page'])?absint($_GET['kb_page']):1);
    $args=['post_type'=>'sachi_article','post_status'=>'publish','s'=>$query,'posts_per_page'=>9,'paged'=>$page];
    if($topic)$args['tax_query']=[['taxonomy'=>'sachi_topic','field'=>'term_id','terms'=>$topic]];
    $articles=new WP_Query($args); $topics=get_terms(['taxonomy'=>'sachi_topic','hide_empty'=>false]);
    ob_start(); ?>
    <section class="sachi-kb"><p class="sachi-eyebrow">Support knowledge base</p><h2>Answers that keep you moving.</h2>
    <form method="get" action="<?php echo esc_url(get_permalink()); ?>" class="sachi-search"><label>Search articles<input name="kb_search" value="<?php echo esc_attr($query); ?>" placeholder="Wi-Fi, endpoint, account…"></label><label>Topic<select name="kb_topic"><option value="0">All topics</option><?php if(!is_wp_error($topics))foreach($topics as $term): ?><option value="<?php echo esc_attr($term->term_id); ?>" <?php selected($topic,$term->term_id); ?>><?php echo esc_html($term->name); ?></option><?php endforeach; ?></select></label><button>Find answers</button></form>
    <div class="sachi-cards"><?php while($articles->have_posts()):$articles->the_post(); ?><article><h3><a href="<?php echo esc_url(get_permalink()); ?>"><?php echo esc_html(get_the_title()); ?></a></h3><p><?php echo esc_html(wp_trim_words(get_the_excerpt(),26)); ?></p><span>Updated <?php echo esc_html(get_the_modified_date()); ?></span></article><?php endwhile; ?></div>
    <?php if(!$articles->post_count): ?><p>No matching articles. Try another keyword or topic.</p><?php endif; ?>
    <nav aria-label="Knowledge base pages"><?php echo wp_kses_post(paginate_links(['base'=>add_query_arg('kb_page','%#%',get_permalink()),'format'=>'','current'=>$page,'total'=>$articles->max_num_pages,'add_args'=>['kb_search'=>$query,'kb_topic'=>$topic],'type'=>'list'])); ?></nav>
    </section><?php wp_reset_postdata(); return ob_get_clean();
});
