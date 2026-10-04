package com.sachibara.inventory;
import org.springframework.context.annotation.*;import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.core.userdetails.*;import org.springframework.security.provisioning.InMemoryUserDetailsManager;import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;import org.springframework.security.config.http.SessionCreationPolicy;
@Configuration public class SecurityConfig {
 @Bean UserDetailsService users(@Value("${inventory.admin-password}") String password){if(password.length()<12)throw new IllegalArgumentException("INVENTORY_ADMIN_PASSWORD must have at least 12 characters.");return new InMemoryUserDetailsManager(User.withUsername("admin").password(new BCryptPasswordEncoder().encode(password)).roles("ADMIN").build());}
 @Bean BCryptPasswordEncoder encoder(){return new BCryptPasswordEncoder();}
 @Bean SecurityFilterChain security(HttpSecurity http)throws Exception{return http.csrf(csrf->csrf.disable()).sessionManagement(s->s.sessionCreationPolicy(SessionCreationPolicy.STATELESS)).authorizeHttpRequests(a->a.requestMatchers("/","/index.html","/app.js","/style.css").permitAll().anyRequest().hasRole("ADMIN")).httpBasic(b->b.authenticationEntryPoint((request,response,error)->{response.setStatus(401);response.setContentType("application/json");response.getWriter().write("{\"error\":\"Authentication required\"}");})).build();}
}
